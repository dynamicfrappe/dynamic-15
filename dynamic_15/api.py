import frappe
from frappe import _
from dynamic_15.cheques.doctype.cheque.cheque import add_row_cheque_tracks

@frappe.whitelist()
def get_active_domains():
	return frappe.get_active_domains()

DOMAINS = frappe.get_active_domains()

@frappe.whitelist()
def submit_journal_entry_cheques(doc):
	if getattr(doc, "payment_entry", None):
		payment_entry = frappe.get_doc("Payment Entry", doc.payment_entry)
		old_status = payment_entry.cheque_status
		payment_entry.cheque_status = doc.cheque_status
		payment_entry.save()
		add_row_cheque_tracks(doc.payment_entry, doc.cheque_status, old_status)

@frappe.whitelist()
def submit_journal_entry(doc, fun=""):
	if "Cheques" in DOMAINS:
		submit_journal_entry_cheques(doc)

@frappe.whitelist()
def update_paymentrntry(doc, *args, **kwargs):
	if "Cheques" in DOMAINS:
		# validate party account with part type

		if doc.endorse_cheque == 1:
			if doc.endorsed_party_type and doc.endorsed_party_account:
				party_type_account_type = frappe.get_doc(
					"Party Type", doc.endorsed_party_type
				).account_type
				part_account_type = frappe.get_doc(
					"Account", doc.endorsed_party_account
				).account_type
				if party_type_account_type != part_account_type:
					party_account = get_party_account(
						doc.endorsed_party_name,
						party=doc.endorsed_party_type,
						company=doc.company,
					)
					# frappe.throw(f"Acoount {party_account}")

					if party_account:
						doc.endorsed_party_account = party_account
					if not party_account:
						if doc.endorsed_party_type == "Customer":
							doc.endorsed_party_account = frappe.get_doc(
								"Company", doc.company
							).default_receivable_account
						if doc.endorsed_party_type == "Supplier":
							doc.endorsed_party_account = frappe.get_doc(
								"Company", doc.company
							).default_payable_account

					frappe.db.commit()
					#  frappe.throw(_(f" Endorsed Party Account type is {party_type_account_type} and party type {doc.endorsed_party_type} "))
					# get defalu party type account