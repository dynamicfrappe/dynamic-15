data = {
	'custom_fields': {
            'Item':[	
                {
				"label": "Width",
				"fieldname": "width",
				"fieldtype": "Float",
				"insert_after": "stock_uom" ,
				},
                {
				"label": "Length",
				"fieldname": "length",
				"fieldtype": "Float",
				"insert_after": "weight" ,
				},
                {
				"label": "Height",
				"fieldname": "height",
				"fieldtype": "Float",
				"insert_after": "length" ,
				},
			],
            'UOM Conversion Detail':[
                {
				"label": "Total",
				"fieldname": "total",
				"fieldtype": "Float",
				"insert_after": "uom" ,
                "read_only" :1 ,
                "in_list_view" : 1
				},
            ]	
	},
		"properties": [
            		
	],  
}