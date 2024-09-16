
from __future__ import unicode_literals
import frappe
from frappe import _

data = {
	'custom_fields': {
		'Stock Entry':[
            {
                "label": "Sales Order",
                "fieldname": "sales_order",
                "fieldtype":"Link",
                "options": "Sales Order",
                "read_only": 1
            },
            {
                "label": "Quotation",
                "fieldname": "quotation",
                "fieldtype":"Link",
                "options": "Quotation",
                "read_only": 1
            }
        ],
        'Sales Order':[
            {
                "label": "Stock Entry",
                "fieldname": "stock_entry",
                "fieldtype":"Link",
                "options": "Stock Entry",
                "read_only": 1
            }
        ],
        'Task':[
            {
                "label": "Delivery Note",
                "fieldname": "delivery_note",
                "fieldtype":"Link",
                "options": "Delivery Note",
                "read_only": 1
            },
            {
                "label": "Attach PDF",
                "fieldname": "attach_pdf",
                "fieldtype":"Attach",
                "insert_after": "description",
            }
        ],
        'Delivery Note':[
            {
                "label": "Task",
                "fieldname": "task",
                "fieldtype":"Link",
                "options": "Task",
                "read_only": 1
            },
            
        ],
        'Delivery Note Item': [
            {
                "label": "Attach Image",
                "fieldname": "attached_image",
                "fieldtype": "Attach Image",
                "insert_after": "item_name",
            }
        ],
        'Purchase Receipt Item': [
            {
                "label": "Attach Image",
                "fieldname": "attached_image",
                "fieldtype": "Attach Image",
                "insert_after": "item_name",
            }
        ],
        'Quotation':[
            {
                "label": "Stock Entry",
                "fieldname": "stock_entry",
                "fieldtype":"Link",
                "options": "Stock Entry",
                "read_only": 1
            }
        ],
	},
	"properties": [
        	
	],  
}