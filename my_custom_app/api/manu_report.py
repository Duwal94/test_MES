import frappe

@frappe.whitelist()
def get_manu_reports():
    from frappe.desk.query_report import run

    partial_dispatch = run("Partial Dispatch Report", filters={})
    to_be_manufactured = run("To Be Manufactured for Delivery", filters={})

    # Only keep JSON-serializable parts
    return {
        "partial_dispatch": {
            "columns": partial_dispatch.get("columns"),
            "result": partial_dispatch.get("result")
        },
        "to_be_manufactured": {
            "columns": to_be_manufactured.get("columns"),
            "result": to_be_manufactured.get("result")
        }
    }

