# Copyright (c) 2024, dynamic business solutions and contributors
# For license information, please see license.txt

from erpnext.accounts.doctype.account.account import get_account_currency
import frappe
from frappe import _
from erpnext.setup.utils import get_exchange_rate
from frappe.model.document import Document
import erpnext
from frappe.utils.data import flt
from frappe.utils import get_link_to_form

DOMAINS = frappe.get_active_domains()


class ReceiptDocument(Document):

    def validate(self):
        self.set_totals()
        if self.difference != 0:
            frappe.msgprint(
                _("Total Difference is {}").format(self.difference))
            frappe.throw(_("Total Difference must be 0"))

    @frappe.whitelist()
    def get_conversion_rate(self):
        company_currency = erpnext.get_company_currency(self.company)
        self.exchange_rate = get_exchange_rate(
            self.currency, company_currency, self.posting_date)

    @frappe.whitelist()
    def set_totals(self):
        self.amount = self.amount or 0
        self.total = 0
        self.difference = self.amount

        precision = frappe.get_precision("Pay and Receipt Account", "amount")
        difference_precision = frappe.get_precision(self.doctype, "difference")
        for item in getattr(self, 'accounts', []):
            item.amount = flt(item.amount or 0, precision)
            item.currency = self.currency
            item.exchange_rate = self.exchange_rate
            item.base_amount = item.amount * self.exchange_rate
            self.total += item.amount
        self.difference = flt(self.amount - self.total, difference_precision)

    def before_insert(self):
        self.journal_entry = ''

    # def validate (self):
    # 	self.journal_entry = ''
    # company_currency = erpnext.get_company_currency(self.company)
    # account_currency = get_account_currency(self.account)
    # if account_currency not in [company_currency , self.currency] :

    def on_submit(self):
        self.create_journal_entry()

    def on_cancel(self):
        self.cancel_journal_entry()

    def create_journal_entry(self):
        company_currency = erpnext.get_company_currency(self.company)
        je = frappe.new_doc("Journal Entry")
        if self.journal_entry_series :
            je.naming_series = self.journal_entry_series
        je.posting_date = self.posting_date
        je.voucher_type = 'Journal Entry'
        je.company = self.company
        je.cheque_no = self.reference_no
        je.cheque_date = self.reference_date
        je.remark = f'Payment against {self.doctype}: ' + \
                    self.name + '\n' + (getattr(self, 'notes', "") or "")
        if 'Maser2000' in DOMAINS:
            je.user_remark = self.notes
            je.cheque_no = self.reference_number
            je.cheque_date = frappe.utils.getdate()
            je.voucher_type = 'Cash Entry' if self.mode_of_payment=="Cash" else 'Bank Entry'
        
        account_currency = get_account_currency(self.account)
        account_exchange_rate = flt(self.exchange_rate)
        amount_in_account_currency = self.amount
        if account_currency != self.currency:
            if account_currency == company_currency:
                account_exchange_rate = 1
                amount_in_account_currency = flt(self.base_amount)

            else:
                account_exchange_rate = get_exchange_rate(
                    account_currency, company_currency, self.posting_date)
                amount_in_account_currency = flt(
                    self.amount) * flt(account_exchange_rate)

        je.append("accounts", {
            "account": self.account,
            "against_account": " , ".join([x.account for x in self.accounts]),
            "account_currency": account_currency,
            "exchange_rate": flt(account_exchange_rate),
            "debit_in_account_currency": flt(amount_in_account_currency),
            "debit_in_company_currency": flt(self.base_amount),
            "reference_type": self.doctype,
            "reference_name": self.name,
            "cost_center": self.cost_center,
            "project": self.project,
            "user_remark": (self.notes or "")
        })
        for account_row in self.accounts:
            account_row_currency = get_account_currency(account_row.account)
            account_row_exchange_rate = flt(account_row.exchange_rate)
            amount_in_account_row_currency = account_row.amount
            if account_row_currency != account_row.currency:
                if account_row_currency == company_currency:
                    account_row_exchange_rate = 1
                    amount_in_account_row_currency = flt(
                        account_row.base_amount)

                else:
                    account_row_exchange_rate = get_exchange_rate(
                        account_currency, company_currency, self.posting_date)
                    amount_in_account_row_currency = flt(
                        account_row.amount) * flt(account_row_exchange_rate)

            je.append("accounts", {
                "account": account_row.account,
                "account_currency": account_row_currency,
                "against_account": self.account,
                "exchange_rate": flt(account_row_exchange_rate),
                "credit_in_account_currency": flt(amount_in_account_row_currency),
                "credit_in_company_currency": flt(account_row.base_amount),
                "cost_center": self.cost_center,
                "project": self.project,
                "user_remark": getattr(account_row, "note", (self.notes or "")),
                "reference_type": self.doctype,
                "reference_name": self.name,
                "party_type": account_row.party_type,
                "party": account_row.party,
                "cost_center": account_row.cost_center,
                "project":account_row.project
            })

        je.multi_currency = 1
        je.submit()
        self.journal_entry = je.name
        self.db_set("journal_entry", je.name)
        lnk = get_link_to_form(je.doctype, je.name)
        frappe.msgprint(_("Journal Entry {} was created").format(lnk))

    def cancel_journal_entry(self):
        if getattr(self, 'journal_entry'):
            je = frappe.get_doc("Journal Entry", self.journal_entry)
            if (je.docstatus == 1):
                je.cancel()
            self.db_set("journal_entry", '')
            gl_entries = frappe.get_all("GL Entry", filters={
                "against_voucher_type": self.doctype,
                "against_voucher": self.name

            })
            # for gl in gl_entries:
            # 	frappe.get_doc("GL Entry", gl).cancel()
            sql = f""" update `tabGL Entry` set  against_voucher_type = '' , against_voucher ='' where  
            against_voucher = '{self.name}' """
            print("sql ================> ",sql)
            frappe.db.sql(sql)
            frappe.db.commit()
@frappe.whitelist()
def get_field_options():
    return {
		"journal_entry_series": frappe.get_meta("Journal Entry").get_options("naming_series"),
		
	}            
