import frappe
from frappe import _
from dynamic_15.cheques.doctype.cheque.cheque import add_row_cheque_tracks
from frappe.utils import getdate


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
def save_item(doc, *args, **kwargs):
	if "UOM" in DOMAINS:
		for item in doc.uoms:
			if item.idx == 1:
				item.total = doc.length * doc.width * doc.height


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


import random
import math
Domains=frappe.get_active_domains()

def get_barcode(digist =False ) :
	if not digist :
		digits = 6 
	numbers = [i for i in range(0, 10)] 
	random_str = ""
	for i in range(digits):
		index = math.floor(random.random() * 10)
		random_str += str(numbers[index])

	return random_str


@frappe.whitelist()
def create_item_barcode(doc ,*args , **kwargs) :
	if "Item Barcode" in Domains:
		barcode = get_barcode()
		if not doc.barcodes :
			row = doc.append("barcodes")
			row.barcode = barcode
			row.uom = doc.stock_uom
		if not doc.custom_barcode or len(doc.custom_barcode) < 3 :
			doc.custom_barcode = barcode


from datetime import datetime 
@frappe.whitelist(allow_guest=False)
def get_sales(*args , **kwargs):
	try:
		if kwargs.get("pos_profile"):
			pos_profile = kwargs.get("pos_profile")
			from_date = datetime.strptime(kwargs.get("from_date"), '%Y-%m-%d')
			to_date = datetime.strptime(kwargs.get("to_date"), '%Y-%m-%d')

			filters = []
			filters.append(("pos_profile","=", pos_profile))
			filters.append(("docstatus","=", 1))
			if from_date :
				filters.append(("posting_date",">=", from_date))

			if to_date:
				filters.append(("posting_date","<=", to_date))

			invoices = frappe.get_list(
				"POS Invoice",
				filters=filters,
				fields=[
					"name as invoice_number",
					"creation as invoice_date",
					"total as invoice_subtotal",
					"total_taxes_and_charges as tax",
					"discount_amount as discount",
					"grand_total as invoice_total"
				],
			)
			return {
				"message":f"""Number of invoices: {len(invoices)}""",
				"data":invoices
			}
	except Exception as e:
		frappe.log_error(message=str(e), title=_('Error in get_sales'))
		frappe.local.response['http_status_code'] = 500

@frappe.whitelist()
def validate_stock_entry(doc, *args, **kwargs):
	if "Real State" in DOMAINS:
		if (
			doc.get("real_state_cost")
			and doc.get("stock_entry_type") == "Material Issue"
		):
			real_stat_cost = frappe.get_doc(
				"Real State Cost", doc.get("real_state_cost")
			)
			for item in real_stat_cost.items:
				for row in doc.items:
					row.item_code == item.item_code
					row.basic_rate = item.amount / item.qty
					row.amount = item.amount
					row.basic_amount = item.amount
	
@frappe.whitelist()
def before_submit_quot(doc, *args, **kwargs):
	if "Real State" in DOMAINS:
		hold_item_reserved(doc, *args, **kwargs)


def before_save_quotation(doc, *args, **kwargs):
	if "Real State" in DOMAINS:
		reserve_unit(doc)
		
		
	if "Dynamic Accounts" in DOMAINS:
		meta = frappe.get_meta(doc.doctype)
		if meta.has_field("outstanding_amount"):
			if len(doc.get("advancess")):
				total_advance_paid = sum(
					adv.advance_amount for adv in doc.get("advancess")
				)
				doc.db_set("advance_paid", total_advance_paid)
				doc.db_set("outstanding_amount", doc.grand_total - total_advance_paid)

def on_cencel(self , *args, **kwargs ):
	if "Real State" in DOMAINS:
		cencel_reserve_unit(self)

def hold_item_reserved(doc, *args, **kwargs):
	for row in doc.items:
		if row.qty > 1:
			frappe.throw(_("Qty Should be 1 "))
		frappe.db.set_value("Item", row.item_code, "reserved", 1)

@frappe.whitelist()
def cencel_reserve_unit(self):
	items = self.get('items')
	for item in items:
		item_obj = frappe.get_doc("Item" , item.item_code)
		item_obj.reserved = 0
		item_obj.save()


@frappe.whitelist()
def reserve_unit(self):
	items = self.get('items')
	for item in items:
		item_obj = frappe.get_doc("Item" , item.item_code)
		item_obj.reserved = 1
		item_obj.save()

@frappe.whitelist()
def before_submit_so(doc, *args, **kwargs):
	if "Real State" in DOMAINS:
		set_advences_to_schedules(doc, *args, **kwargs)

@frappe.whitelist()
def set_advences_to_schedules(doc, *args, **kwargs):
	total_advance = 0
	if doc.advancess:
		total_advance = 0
		for advance in doc.advancess:
			total_advance += advance.allocated_amount
	if doc.payment_schedule:
		for schedule in doc.payment_schedule:
			if (
				total_advance > 0
				and (schedule.outstanding - (schedule.paid_amount or 0)) > 0
			):
				advance_added_amount = schedule.outstanding - (
					schedule.paid_amount or 0
				)
				if advance_added_amount >= total_advance:
					schedule.db_set(
						"paid_amount", (schedule.paid_amount or 0) + total_advance
					)
					total_advance = 0
				elif advance_added_amount < total_advance:
					schedule.db_set(
						"paid_amount",
						(schedule.paid_amount or 0) + advance_added_amount,
					)
					total_advance -= advance_added_amount
