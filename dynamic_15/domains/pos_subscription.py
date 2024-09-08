from __future__ import unicode_literals
import frappe
from frappe import _

data = {

    'custom_fields': {
        "POS Profile":[
            {
                "fieldname": "otp",
                "fieldtype": "Data",
                "insert_after": "disabled",
                "label": "OTP",
            },
        ]
    },
      "properties": [
        {
            "doctype": "POS Profile",
            "doctype_or_field": "DocField",
            "fieldname": "disabled",
            "property": "read_only",
            "property_type": "Check",
            "value": "1",
        },
        {
            "doctype": "POS Profile",
            "doctype_or_field": "DocField",
            "fieldname": "disabled",
            "property": "default",
            "value": "1",
        },
    ],
  
}

