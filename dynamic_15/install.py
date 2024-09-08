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
	if not frappe.db.exists("Domain", "UOM"):
		dm1 = frappe.new_doc("Domain")
		dm1.domain = 'UOM'
		dm1.insert()
	if not frappe.db.exists("Domain", "Item Barcode"):
		dm1 = frappe.new_doc("Domain")
		dm1.domain = 'Item Barcode'
		dm1.insert()
	if not frappe.db.exists("Domain", "POS Subscription"):
		dm1 = frappe.new_doc("Domain")
		dm1.domain = 'POS Subscription'
		dm1.insert()
	if not frappe.db.exists("Domain", "Dynamic Accounts"):
		try:
			dm = frappe.get_doc({
				"doctype": "Domain",
				"domain": "Dynamic Accounts"
			})
			dm.insert()
			frappe.db.commit()
		except frappe.DuplicateEntryError:
			print("Domain 'Dynamic Accounts' already exists.")
		except Exception as e:
			print(f"An error occurred: {e}")
			frappe.db.rollback()
			
	if not frappe.db.exists("Domain", "Cheques"):
		try:
			dm = frappe.get_doc({
				"doctype": "Domain",
				"domain": "Cheques"
			})
			dm.insert()
			frappe.db.commit()
		except frappe.DuplicateEntryError:
			print("Domain 'Cheques' already exists.")
		except Exception as e:
			print(f"An error occurred: {e}")
			frappe.db.rollback()