from erpnext.stock.doctype.stock_entry.stock_entry import StockEntry as OriginalStockEntry
import frappe
from frappe import _



class StockEntry(OriginalStockEntry):
    Domains=frappe.get_active_domains()
    if "Tebian"  in Domains :
        def validate(self):
            super(StockEntry, self).validate()
            self.validate_finished_goods()

    def validate_finished_goods(self):
        pass
