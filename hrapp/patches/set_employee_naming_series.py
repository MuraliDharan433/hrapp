import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def execute():
	# New employees get IDs like "INF-001" instead of the default "HR-EMP-00001".
	# Existing employee IDs are not renamed.
	make_property_setter(
		"Employee",
		"naming_series",
		"options",
		"INF-.###",
		"Text",
		validate_fields_for_doctype=False,
	)
	make_property_setter(
		"Employee",
		"naming_series",
		"default",
		"INF-.###",
		"Text",
		validate_fields_for_doctype=False,
	)
	frappe.clear_cache(doctype="Employee")
