import frappe

def execute():
    # We move this script natively to public/js/stock_entry.js
    if frappe.db.exists("Client Script", "Fetching Total Bags Qty"):
        frappe.delete_doc("Client Script", "Fetching Total Bags Qty", ignore_permissions=True)
