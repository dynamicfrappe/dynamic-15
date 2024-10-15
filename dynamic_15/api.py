import frappe
from frappe import _
from dynamic_15.cheques.doctype.cheque.cheque import add_row_cheque_tracks
from erpnext.controllers.accounts_controller import get_advance_journal_entries, get_advance_payment_entries
from erpnext.accounts.party import get_party_account
from frappe.utils import add_days, cint, cstr, flt, get_link_to_form, getdate, nowdate, strip_html


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


@frappe.whitelist()
def get_advanced_so_ifi(doc_name):
	"""Returns list of advances against Account, Party, Reference"""
	self = frappe.get_doc('Sales Order', doc_name)
	res = get_advance_entries(self)
	self.set("advancess", [])
	# print('\n\n\n-->res:',res)
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
		

		# self.append("advancess", advance_row)
	# print('\n\n\n-->after update:',res)
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
	if isinstance(party_account, str):
		party_account = [party_account]
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
	if isinstance(party_account, str):
		party_account = [party_account]

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

@frappe.whitelist()
def check_calculate_weight(doc, *args, **kwargs):
	if "Tebian" in DOMAINS:
		sum = 0
		for item in doc.items :
			if item.item_code :
				calculate_weight = frappe.db.get_value(
							"Item", {"name": item.item_code}, "calculate_weight")
				item.calculate_weight = calculate_weight
				if item.calculate_weight :
					set_total_weight(item)

				if item.is_finished_item or item.is_scrap_item :
					item.has_weight = 1
				if item.is_finished_item == 0 :
					sum += item.total_weight
				if item.has_weight :
					item.total_weight = sum
					item.weight_rate = sum / item.qty

@frappe.whitelist()
def validat_stock_qty(doc, *args, **kwargs):
	if doc.stock_entry_type == "Cuting" :
		diff = 0
		scrap =''
		conversion_factor = 0.0
		basic_rate = 0.0
		for item in doc.items : 
			if item.scrap_item:
				basic_rate = item.basic_rate
				scrap = item.scrap_item 
			diff = abs(abs(diff) - item.transfer_qty)
		if diff !=0:
			item = frappe.get_doc("Item" , scrap)
			for uom in item.uoms :
				if uom.uom == item.stock_uom :
					conversion_factor = uom.conversion_factor
			doc.append("items" , {
				"item_code" : scrap ,
				"qty" : diff ,
				"uom" : item.stock_uom ,
				"transfer_qty" : conversion_factor ,
				"stock_uom" : item.stock_uom ,
				"conversion_factor" : conversion_factor ,
				"is_finished_item" : 1 ,
				"basic_rate" : basic_rate ,
			})
		for item in doc.items : 
			item.basic_rate = basic_rate
		


	

def set_total_weight(item):
	if item.stock_uom == item.uom :
		item.total_weight = item.weight_per_unit * item.qty 
	else :
		item.total_weight = item.weight_per_unit * item.transfer_qty 



def set_total_weight(item):
	if item.stock_uom == item.uom :
		item.total_weight = item.weight_per_unit * item.qty 
	else :
		item.total_weight = item.weight_per_unit * item.transfer_qty 


@frappe.whitelist()
def create_stock_entry(source):
	material_request = frappe.get_doc("Material Request" , source)
	stock_entry = frappe.new_doc("Stock Entry")
	stock_entry.stock_entry_type = material_request.material_request_type
	stock_entry.to_warehouse = material_request.set_warehouse
	stock_entry.material_request = material_request.name
	for item in material_request.items :
		stock_entry.append("items" , {
			"t_warehouse" :  material_request.set_warehouse , 
			"item_code" : item.item_code ,
			"item_name" : item.item_name,
			"description" : item.description ,
			"uom" : item.uom ,
			"basic_rate" : item.rate ,
			"qty" : item.qty ,
			"stock_uom" : item.stock_uom ,
			"transfer_qty" : item.stock_qty,
			"is_finished_item" : 1,
			"has_weight" : 1 ,
			"conversion_factor" : item.conversion_factor
		})
	return stock_entry