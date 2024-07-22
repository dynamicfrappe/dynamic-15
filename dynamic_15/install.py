import frappe
import os
import json

def after_install():
	print("Dynamic Business Solutions")
	create_domain_list()
	

def create_domain_list():
	if not frappe.db.exists("Domain", "Tebian"):
		dm1 = frappe.new_doc("Domain")
		dm1.domain = 'Tebian'
		dm1.insert()