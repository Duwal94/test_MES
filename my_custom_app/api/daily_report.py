import frappe
from frappe.utils import today
from frappe.desk.query_report import run

@frappe.whitelist()
def get_reports(from_date=None, to_date=None):
    # Step 1: Ensure default dates
    from_date = str(from_date) if from_date else today()
    to_date = str(to_date) if to_date else today()

    # Step 2: Always start with a proper dict mapping
    date_filters = {"from_date": from_date, "to_date": to_date}

    reports = {
        "stitching": "Stitching Work Today",
        "cutting": "Cutting Section",
        "quilting": "Quilting Section",
        "pillow": "Pillow Section",
        "dispatch": "Dispatch Report",
        "Pending Delivery Note": "Delivery Note",
    }

    output = {}

    for key, report_name in reports.items():
        try:
            # Get the report doc
            report_doc = frappe.get_doc("Report", report_name)

            # Step 3: Initialize filters as a dict
            filters = date_filters.copy()

            # Step 4: Check if the report is a query report
            if getattr(report_doc, "report_type", None) == "Query Report":
                query = getattr(report_doc, "query", "") or ""
                # Only use date_filters if placeholders exist in the query
                if "%(from_date)" not in query or "%(to_date)" not in query:
                    filters = {}

            # Step 5: Force known reports to use date filters
            if report_name in ["Stitching Work Today", "Cutting Section", "Dispatch Report"]:
                filters = {**date_filters, **filters}

            # Step 6: Ultimate safety net
            if not isinstance(filters, dict):
                filters = date_filters.copy()

            # Step 7: Ensure keys exist with valid values
            filters["from_date"] = filters.get("from_date") or today()
            filters["to_date"] = filters.get("to_date") or today()

            # Step 8: Run the report
            result = run(report_name, filters=filters)

            # Step 9: Store output
            output[key] = {
                "columns": result.get("columns", []),
                "result": result.get("result", []),
                "filters_used": filters,
                "status": "ok",
            }

        except Exception as e:
            frappe.log_error(frappe.get_traceback(), f"Error running report {report_name}")
            output[key] = {
                "columns": [],
                "result": [],
                "status": "error",
                "error_message": str(e),
            }

    return output

