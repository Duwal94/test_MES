import frappe
from frappe.email.doctype.email_queue.email_queue import send_now

def send_all_pending_emails():
    pending_emails = frappe.get_all("Email Queue", filters={"status": "Not Sent"}, pluck="name")
    for email_name in pending_emails:
        try:
            send_now(email_name)
            frappe.logger().info(f"Sent email: {email_name}")
        except Exception as e:
            frappe.log_error(f"Error sending email {email_name}: {e}")

