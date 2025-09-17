import frappe

@frappe.whitelist()
def get_bom_operations(bom_no):
    return frappe.get_all(
        "BOM Operation",
        filters={"parent": bom_no},
        fields=["operation", "workstation", "time_in_mins", "description", "idx"],
        order_by="idx"
    )

