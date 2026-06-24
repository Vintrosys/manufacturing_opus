frappe.ui.form.on("Stock Entry", {
    refresh: function(frm) {
        if (frm.doc.docstatus === 0) {
            fetch_work_order_details(frm);
        }
    },

    work_order: function(frm) {
        if (frm.doc.docstatus === 0) {
            fetch_work_order_details(frm);
        }
    }
});

function fetch_work_order_details(frm) {
    if (!frm.doc.work_order) return;

    frappe.db.get_doc("Work Order", frm.doc.work_order)
        .then(doc => {
            frm.set_value("custom_packing_size", doc.custom_packing_size);
            frm.set_value("custom_total_bags", doc.custom_total_bags);
            frm.set_value(
                "custom_jumbo_bag_item",
                doc.custom_jumbo_bag_item
            );
        });
}
