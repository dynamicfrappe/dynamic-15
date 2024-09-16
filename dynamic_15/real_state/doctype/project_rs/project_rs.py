# Copyright (c) 2024, dynamic business solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProjectRS(Document):
	pass

@frappe.whitelist()
def create_stage(project_name):
	new_stage = frappe.new_doc("Project RS Stages")
	new_stage.project_name = project_name
	return new_stage
