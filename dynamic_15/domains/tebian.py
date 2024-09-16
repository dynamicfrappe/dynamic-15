from __future__ import unicode_literals
import frappe
from frappe import _

data = {
	'custom_fields': {
			'Stock Entry Detail':[	
                {
				"label": "Weight Per Unit",
				"fieldname": "weight_per_unit",
				"fieldtype": "Float",
				"insert_after": "retain_sample" ,
				"fetch_from": "item_code.weight_per_unit"
				},
                {
				"label": "Weight UOM",
				"fieldname": "weight_uom",
				"fieldtype": "Link",
                "options":"UOM",
				"insert_after": "weight_per_unit" ,
				"fetch_from": "item_code.weight_uom"
				},
                {
				"label": "has Weight",
				"fieldname": "has_weight",
				"fieldtype": "Check",
				"insert_after": "uom" ,
				},
                {
				"label": "Weight rate",
				"fieldname": "weight_rate",
				"fieldtype": "Float",
				"insert_after": "has_weight" ,
                "fetch_from": "item_code.weight_rate"
				},
                {
				"label": "Total Weight",
				"fieldname": "total_weight",
				"fieldtype": "Float",
				"insert_after": "weight_rate" ,
				},
                {
				"label": "Calculate Weight",
				"fieldname": "calculate_weight",
				"fieldtype": "Check",
				"insert_after": "total_weight" ,
				},
			],
            'Item':[	
                {
				"label": "Weight Rate",
				"fieldname": "weight_rate",
				"fieldtype": "Float",
				"insert_after": "stock_uom" ,
				},
                 {
				"label": "Calculate Weight",
				"fieldname": "calculate_weight",
				"fieldtype": "Check",
				"insert_after": "weight_rate" ,
				},
			],
            'Customer':[	
                {
				"label": "Categories",
				"fieldname": "categories",
				"fieldtype": "Link",
                "options":"Categories",
				"insert_after": "market_segment" ,
				},
                {
				"label": "Commerical Number",
				"fieldname": "commerical_number",
				"fieldtype": "Data",
				"insert_after": "tax_id" ,
				},
                {
				"label": "Customer Name in English",
				"fieldname": "customer_name_in_english",
				"fieldtype": "Data",
				"insert_after": "customer_name" ,
				},
			],	
	},
		"properties": [
            		
	],  
}