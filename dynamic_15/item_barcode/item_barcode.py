import frappe 
from frappe import _ 

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