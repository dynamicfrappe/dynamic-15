

from __future__ import unicode_literals
import frappe
from frappe import _

data = {

    'custom_fields': {
        'Stock Entry':[
            {
                "label":_("Real State Cost"),
                "fieldname":"real_state_cost",
                "fieldtype":"Link",
                "options":"Real State Cost",
                "read_only":"1", 
                "insert_after":"total_amount", 
            },
        ],
        'Landed Cost Taxes and Charges':[
            {
                "label":_("Cost Center"),
                "fieldname":"taxes_cost_center",
                "fieldtype":"Link",
                "insert_after":"base_amount", 
                "options":"Cost Center", 
                "in_list_view":"1", 
            },
        ],
        'Lead':[
            {
                "label":_("Call Type"),
                "fieldname":"call_type",
                "fieldtype":"Select",
                "insert_after":"contact_by", 
                "options":"\nFresh Call\nCold Call",
            },
        ],
        'Opportunity':[
            {
                "label":_("Note"),
                "fieldname":"note",
                "fieldtype":"Small Text",
                "insert_after":"source", 
            },
        ],
        'Item':[
            {
                "label":_("Unit Info"),
                "fieldname":"unit_info",
                "fieldtype":"Section Break",
                "insert_after":"image", 
            },
            {
                "label":_("Unit No"),
                "fieldname":"unit_no",
                "fieldtype":"Int",
                "insert_after":"unit_info", 
            },
            {
                "label":_("Unit Area"),
                "fieldname":"unit_area",
                "fieldtype":"Float",
                "insert_after":"unit_no", 
            },
            {
                "label":_("Unit Floor"),
                "fieldname":"unit_floor",
                "fieldtype":"Int",
                "insert_after":"unit_area", 
            },
            {
                "label":_("Unit Floor Text"),
                "fieldname":"unit_floor_text",
                "fieldtype":"Data",
                "insert_after":"unit_floor", 
            },
            {
                "label":_("Reserved"),
                "fieldname":"reserved",
                "fieldtype":"Check",
                "insert_after":"unit_floor_text", 
                "read_only":"1", 
            },
            {
                "label":_("Unit details"),
                "fieldname":"unit_details",
                "fieldtype":"Small Text",
                "insert_after":"reserved", 
            },
        ],   
    },
      "properties": [
         {
            "doctype": "Payment Terms Template Detail",
            "doctype_or_field": "DocField",
            "fieldname": "due_date_based_on",
            "property": "default",
            "property_type": "Text",
            "value": "Month(s) after the end of the invoice month",
        },
        {
            "doctype": "Quotation",
            "doctype_or_field": "DocField",
            "fieldname": "ignore_pricing_rule",
            "property": "hidden",
            "property_type": "Check",
            "value": "1",
        },
        # {
        #     "doctype": "Lead",
        #     "doctype_or_field": "DocField",
        #     "fieldname": "notes",
        #     "property": "reqd",
        #     "property_type": "Check",
        #     "value": "1",
        # },
    ],
}







