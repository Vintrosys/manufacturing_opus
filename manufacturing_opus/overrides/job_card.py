from erpnext.manufacturing.doctype.job_card.job_card import JobCard
import frappe
from frappe.utils import flt, cint, get_link_to_form
from erpnext.manufacturing.doctype.work_order.work_order import make_stock_entry
import json
from frappe import _
from erpnext.accounts.doctype.pos_invoice.pos_invoice import get_stock_availability
from frappe import _, bold
from typing import Union


class OperationSequenceError(frappe.ValidationError):
    pass


class JC(JobCard):
    def on_update(self):
        self.validate_job_card_qty()
        self.validate_time_logs()
        self.set_status()
        self.validate_operation_id()
        self.validate_sequence_id()
        self.set_sub_operations()
        self.update_sub_operation_status()
        self.validate_work_order()
        self.update_work_order()

    def validate(self):
        self.validate_time_logs()
        self.set_status()
        self.validate_operation_id()
        self.validate_sequence_id()
        self.set_sub_operations()
        self.update_sub_operation_status()
        self.validate_work_order()
        self.update_work_order()

    def on_submit(self):
        self.validate_transfer_qty()
        self.validate_job_card()
        self.update_work_order()
        self.set_transferred_qty()
        if self.for_quantity != self.total_completed_qty:
            frappe.throw(_("Kindly Complete Planned Qty and Submit"))

    def get_current_operation_data(self):
        return frappe.db.sql(
            """
            SELECT
                sum(total_time_in_mins) as time_in_mins,
                sum(total_completed_qty) as completed_qty,
                sum(process_loss_qty) as process_loss_qty
            FROM `tabJob Card`
            WHERE
                docstatus != 2
                AND work_order = %s
                AND operation_id = %s
                AND is_corrective_job_card = 0
            """,
            (self.work_order, self.operation_id),
            as_dict=1,
        )

    def validate_produced_quantity(self, for_quantity, process_loss_qty, wo):
        """Override to accept wo parameter"""
        pass

    def update_work_order_data(self, for_quantity, process_loss_qty, time_in_mins, wo):
        """Override to accept wo parameter"""
        pass

    def validate_sequence_id(self):
        return

    def update_work_order(self):
        if not self.work_order:
            return

        if self.is_corrective_job_card and not cint(
            frappe.db.get_single_value(
                "Manufacturing Settings",
                "add_corrective_operation_cost_in_finished_good_valuation",
            )
        ):
            return

        for_quantity, time_in_mins, process_loss_qty = 0, 0, 0

        data = self.get_current_operation_data()
        if data and len(data) > 0:
            for_quantity = flt(data[0].completed_qty)
            time_in_mins = flt(data[0].time_in_mins)
            if self.docstatus != 1:
                process_loss_qty = 0

        wo = frappe.get_doc("Work Order", self.work_order)

        if self.is_corrective_job_card:
            self.update_corrective_in_work_order(wo)

        self.validate_produced_quantity(for_quantity, process_loss_qty, wo)
        self.update_work_order_data(for_quantity, process_loss_qty, time_in_mins, wo)

        if self.docstatus == 1:
            needs_save = False
            for row in wo.operations:
                if row.name == self.operation_id and row.status != "Completed":
                    row.status = "Completed"
                    needs_save = True
            
            if needs_save:
                wo.flags.ignore_validate_update_after_submit = True
                wo.save(ignore_permissions=True)


@frappe.whitelist()
def make_time_log(args: Union[dict, str]) -> None:
    if isinstance(args, str):
        args = json.loads(args)

    args = frappe._dict(args)
    doc = frappe.get_doc("Job Card", args.job_card_id)
    doc.validate_sequence_id()

    # Ensure complete_time is set so the time log closes
    if not args.get("complete_time") and args.get("action") == "Complete":
        args["complete_time"] = frappe.utils.now_datetime()

    if args.get("for_quantity"):
        doc.for_quantity = flt(args.get("for_quantity"))
    if args.get("process_loss_qty") is not None:
        doc.process_loss_qty = flt(args.get("process_loss_qty"))

    doc.add_time_log(args)
    
    # We must save the document to update total_completed_qty and other fields
    doc.save(ignore_permissions=True)

    wo = frappe.get_doc("Work Order", doc.work_order)
    completed_qty = flt(args.get("completed_qty"))

    if not completed_qty:
        return

    if doc.sequence_id and doc.sequence_id > 1:
        current_op_idx = -1
        for i, op in enumerate(wo.operations):
            if op.name == doc.operation_id:
                current_op_idx = i
                break
                
        if current_op_idx > 0:
            prev_op = wo.operations[current_op_idx - 1]
            current_op = wo.operations[current_op_idx]
            if prev_op.completed_qty < current_op.completed_qty:
                frappe.throw(
                    _(
                        "Excess Production not allowed. Kindly Complete Previous "
                        "Operations Qty before Completing this Operation Qty"
                    )
                )

    is_last_operation = doc.sequence_id == len(wo.operations)

    if is_last_operation:
        if len(wo.operations) != 1:
            prev_op = wo.operations[-2]
            current_op = wo.operations[-1]
            if prev_op.completed_qty < current_op.completed_qty:
                frappe.throw(
                    _(
                        "Excess Production not allowed. Kindly Complete Previous "
                        "Operations Qty before Completing Finished Good Qty"
                    )
                )

        se, action = _make_manufacture_stock_entry(wo, doc, completed_qty)

        frappe.msgprint(
            msg="""
                <b>Stock Entry {action}:</b><br>
                <a href="/app/stock-entry/{name}" target="_blank">{name}</a>
            """.format(action=action, name=se.name),
            title="Success",
            indicator="green",
        )

    remaining = flt(doc.for_quantity) - flt(doc.total_completed_qty)
    if remaining > 0.001:
        frappe.db.set_value(
            "Job Card",
            doc.name,
            "status",
            "Open",
            update_modified=False,
        )


def _make_manufacture_stock_entry(wo, job_card_doc, newly_completed_qty):
    """
    Build a Manufacture Stock Entry directly from BOM.
    Always creates a new Draft entry for each partial completion.
    """
    se = frappe.new_doc("Stock Entry")
    se.stock_entry_type    = "Manufacture"
    se.purpose             = "Manufacture"
    se.work_order          = wo.name
    se.job_card            = job_card_doc.name
    se.company             = wo.company
    se.posting_date        = frappe.utils.today()
    se.posting_time        = frappe.utils.nowtime()
    se.from_bom            = 1
    se.bom_no              = wo.bom_no
    se.fg_completed_qty    = flt(newly_completed_qty)
    se.use_multi_level_bom = wo.use_multi_level_bom

    qty_to_append = flt(newly_completed_qty)
    bom = frappe.get_doc("BOM", wo.bom_no)
    is_last_op = job_card_doc.sequence_id == len(wo.operations)

    # ── Finished Good row — only on the last operation ──────────────
    if is_last_op:
        se.append("items", {
            "item_code":        wo.production_item,
            "qty":              qty_to_append,
            "t_warehouse":      wo.fg_warehouse,
            "is_finished_item": 1,
        })

    # ── Raw Material rows — proportional to BOM qty ─────────────────
    bom_qty = flt(bom.quantity) or 1
    ratio   = qty_to_append / bom_qty

    for item in bom.items:
        required_qty = flt(item.qty) * ratio
        if required_qty <= 0:
            continue
        se.append("items", {
            "item_code":              item.item_code,
            "qty":                    required_qty,
            "uom":                    item.uom,
            "stock_uom":              item.stock_uom,
            "conversion_factor":      item.conversion_factor or 1,
            "s_warehouse":            wo.wip_warehouse or item.source_warehouse,
            "allow_alternative_item": item.allow_alternative_item,
        })

    se.flags.ignore_job_card_check = True
    se.insert(ignore_permissions=True)
        
    return se, "Created"


@frappe.whitelist()
def get_mtfm_items(work_order: str) -> list:
    wo = frappe.get_doc("Work Order", work_order)
    items = []
    for row in wo.required_items:
        if row.transferred_qty and row.consumed_qty < row.transferred_qty:
            stock_status = get_stock_availability(row.item_code, wo.wip_warehouse)
            unconsumed_qty = row.transferred_qty - row.consumed_qty
            if stock_status[0] >= unconsumed_qty:
                items.append({
                    "item_code":   row.item_code,
                    "allowed_qty": unconsumed_qty,
                    "s_warehouse": wo.wip_warehouse,
                    "t_warehouse": row.source_warehouse,
                    "uom":         row.stock_uom,
                    "stock_uom":   row.stock_uom,
                })
            else:
                items.append({
                    "item_code":   row.item_code,
                    "allowed_qty": stock_status[0],
                    "s_warehouse": wo.wip_warehouse,
                    "t_warehouse": row.source_warehouse,
                    "uom":         row.stock_uom,
                    "stock_uom":   row.stock_uom,
                })
    return items


@frappe.whitelist()
def create_material_transfer(work_order: str, items: Union[list, str], job_card: str) -> None:
    items = frappe.parse_json(items)

    new_se = frappe.new_doc("Stock Entry")
    new_se.stock_entry_type = "Material Transfer"
    new_se.company          = frappe.db.get_value("Work Order", work_order, "company")
    new_se.work_order       = work_order
    new_se.posting_date     = frappe.utils.today()
    new_se.custom_rm_job_card = job_card

    for row in items:
        if row["qty"] > row["allowed_qty"]:
            frappe.throw(_(f"Excess Qty not allowed for {row['item_code']}"))
            return
        new_se.append("items", {
            "item_code":  row["item_code"],
            "qty":        row["qty"],
            "uom":        row["uom"],
            "stock_uom":  row["stock_uom"],
            "s_warehouse": row["s_warehouse"],
            "t_warehouse": row["t_warehouse"],
        })

    se = frappe.get_doc(new_se.as_dict())
    se.insert(ignore_permissions=True)
    frappe.msgprint(
        msg="""
            <b>Stock Entry Created:</b><br>
            <a href="/app/stock-entry/{name}" target="_blank">{name}</a>
        """.format(name=se.name),
        title="Success",
        indicator="green",
    )


@frappe.whitelist()
def force_submit_job_card(job_card: str) -> str:
    doc = frappe.get_doc("Job Card", job_card)
    doc.for_quantity = doc.total_completed_qty
    doc.save(ignore_permissions=True)
    doc.submit()
    return "Success"