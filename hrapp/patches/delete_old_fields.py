import frappe

def execute():
    # Delete custom field
    if frappe.db.exists("Custom Field", "Employee-old_field_name"):
        frappe.delete_doc("Custom Field", "Employee-old_field_name")

    # Delete notification
    if frappe.db.exists("Notification", "Test Notification"):
        frappe.delete_doc("Notification", "Test Notification")

    # Delete workflow
    if frappe.db.exists("Workflow", "Old Workflow"):
        frappe.delete_doc("Workflow", "Old Workflow")