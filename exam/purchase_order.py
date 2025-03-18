import frappe
from frappe.utils import now_datetime

def on_update(doc, method):

	if doc.workflow_state and not frappe.flags.get("is_approval_log_updated"):
		approver_name = frappe.session.user
		approval_stage = doc.workflow_state
		timestamp = now_datetime()

		doc.append("approval_logs", {
			"approver_name": approver_name,
			"approval_stage": approval_stage,
			"timestamp": timestamp

		})

		frappe.flags.is_approval_log_updated = True
		doc.save(ignore_permissions=True)
