

from erpnext.controllers.accounts_controller import get_advance_journal_entries, get_advance_payment_entries
import frappe
from frappe import _
from frappe.utils import flt, getdate, nowdate
import json
from frappe.utils import get_url
from erpnext.accounts.party import get_party_account
from erpnext.accounts.party import get_party_account_currency
from frappe.utils import add_days, cint, cstr, flt, get_link_to_form, getdate, nowdate, strip_html



DOMAINS = frappe.get_active_domains()


@frappe.whitelist()
def get_advanced_so_ifi(doc_name):
	"""Returns list of advances against Account, Party, Reference"""
	self = frappe.get_doc('Sales Order', doc_name)
	res = get_advance_entries(self)
	self.set("advancess", [])
	advance_allocated = 0
	for d in res:
		if d.against_order:
			allocated_amount = flt(d.amount)
			d['allocated_amount'] = allocated_amount
		else:
			if self.get("party_account_currency") == self.company_currency:
				amount = self.get(
					"base_rounded_total") or self.base_grand_total
			else:
				amount = self.get("rounded_total") or self.grand_total

			allocated_amount = min(amount - advance_allocated, d.amount)
			d['allocated_amount'] = allocated_amount
		advance_allocated += flt(allocated_amount)
		
	return res



def get_advance_entries(self, include_unallocated=True):
	if self.doctype == "Sales Invoice":
		party_account = self.debit_to
		party_type = "Customer"
		party = self.customer
		amount_field = "credit_in_account_currency"
		order_field = "sales_order"
		order_doctype = "Sales Order"
	elif self.doctype == "Sales Order":
		party_account = get_party_account("Customer", party=self.customer, company=self.company)
		party_type = "Customer"
		party = self.customer
		amount_field = "credit_in_account_currency"
		order_field = "sales_order"
		order_doctype = "Sales Order"
	else:
		party_account = self.credit_to
		party_type = "Supplier"
		party = self.supplier
		amount_field = "debit_in_account_currency"
		order_field = "purchase_order"
		order_doctype = "Purchase Order"

	# print('\n\n-->party_type',party_account)
	# order_list = list(set(d.get(order_field) for d in self.get("items") if d.get(order_field)))
	order_list = [self.name, ]
	journal_entries = get_advance_journal_entries(
		party_type, party, party_account, amount_field, order_doctype, order_list, include_unallocated
	)

	payment_entries = get_advance_payment_entries(
		party_type, party, party_account, order_doctype, order_list, include_unallocated
	)

	res = journal_entries + payment_entries

	return res



@frappe.whitelist()
def get_advance_entries_quotation(doc_name, include_unallocated=True):
		self = frappe.get_doc('Quotation', doc_name)
		if self.doctype == "Sales Invoice":
			party_account = self.debit_to
			party_type = "Customer"
			party = self.customer
			amount_field = "credit_in_account_currency"
			order_field = "sales_order"
			order_doctype = "Sales Order"
		elif self.doctype == "Quotation":
			party_account = get_party_account("Customer", party=self.party_name, company=self.company)
			print("party_account = " ,party_account)
			party_type = "Customer"
			party = self.party_name
			amount_field = "credit_in_account_currency"
			order_field = ""
			order_doctype = "Sales Invoice"
		else:
			party_account = self.credit_to
			party_type = "Supplier"
			party = self.supplier
			amount_field = "debit_in_account_currency"
			order_field = "purchase_order"
			order_doctype = "Purchase Order"

		order_list = []

		journal_entries = get_advance_journal_entries(
			party_type, party, party_account, amount_field, order_doctype, order_list, include_unallocated
		)
		print("journal_entries = ",journal_entries)

		payment_entries = get_advance_payment_entries(
			party_type, party, party_account, order_doctype, order_list, include_unallocated
		)
		print("payment_entries = ",payment_entries)

		res = journal_entries + payment_entries

		return res

