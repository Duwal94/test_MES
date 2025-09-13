import frappe

@frappe.whitelist()
def get_reports():
    from frappe.desk.query_report import run

    stitching = run("Stitching Work Today", filters={})
    cutting = run("Cutting Section", filters={})
    quilting = run("Quilting Section", filters={})
    pillow = run("Pillow Section", filters={})
    dispatch = run("Dispatch Report", filters={})
    pending = run("Pending Report", filters={})

    # Only keep JSON-serializable parts
    return {
        "stitching": {
            "columns": stitching.get("columns"),
            "result": stitching.get("result")
        },
        "cutting": {
            "columns": cutting.get("columns"),
            "result": cutting.get("result")
        },
        "quilting": {
            "columns": quilting.get("columns"),
            "result": quilting.get("result")
        },
        "pillow": {
            "columns": pillow.get("columns"),
            "result": pillow.get("result")
        },
        "dispatch": {
            "columns": dispatch.get("columns"),
            "result": dispatch.get("result")
        },
        "pending": {
            "columns": pending.get("columns"),
            "result": pending.get("result")
        }
    }
