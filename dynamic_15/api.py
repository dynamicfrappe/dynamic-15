import frappe
from frappe import _

@frappe.whitelist()
def get_active_domains():
	return frappe.get_active_domains()