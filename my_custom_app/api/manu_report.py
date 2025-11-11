import frappe
from frappe.utils import today
from frappe.desk.query_report import run

@frappe.whitelist()
def get_manufacturing_reports(from_date=None, to_date=None):
    """Fetch manufacturing-related reports with enforced date filters."""
    
    # Step 1: Default to today's date if not provided
    from_date = str(from_date) if from_date else today()
    to_date = str(to_date) if to_date else today()

    # Step 2: Base date filters
    date_filters = {"from_date": from_date, "to_date": to_date}

    # Step 3: Manufacturing reports mapping
    reports = {
        "partial_dispatch": "Partial Dispatch Report",
        "to_be_manufactured": "To Be Manufactured for Delivery",
    }

    output = {}

    # Step 4: Iterate through reports
    for key, report_name in reports.items():
        try:
            # Fetch the report document
            report_doc = frappe.get_doc("Report", report_name)

            # Initialize filters
            filters = date_filters.copy()

            # Step 5: Handle Query Reports specifically
            if getattr(report_doc, "report_type", None) == "Query Report":
                query = getattr(report_doc, "query", "") or ""
                # Use date filters only if placeholders exist
                if "%(from_date)" not in query or "%(to_date)" not in query:
                    filters = {}

            # Step 6: Enforce date filters for known manufacturing reports
            if report_name in [
                "Partial Dispatch Report",
                "To Be Manufactured for Delivery",
            ]:
                filters = {**date_filters, **filters}

            # Step 7: Validate filters
            if not isinstance(filters, dict):
                filters = date_filters.copy()

            filters["from_date"] = filters.get("from_date") or today()
            filters["to_date"] = filters.get("to_date") or today()

            # Step 8: Execute report
            result = run(report_name, filters=filters)

            # Step 9: Store result
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

