import frappe


def execute():
	# hrapp.patches.delete_old_fields tried to remove these but missed: the
	# notification kept getting recreated by fixture sync (still declared in
	# notification.json), and the workflow name it checked ("Old Workflow")
	# never matched the actual leftover ("Test Workflow"). Both have now been
	# removed from the fixture files too, so this cleans up sites where the
	# buggy patch already ran and won't fire again.
	if frappe.db.exists("Notification", "Test Notification"):
		frappe.delete_doc("Notification", "Test Notification")

	if frappe.db.exists("Workflow", "Test Workflow"):
		frappe.delete_doc("Workflow", "Test Workflow")
