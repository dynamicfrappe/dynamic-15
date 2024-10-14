app_name = "dynamic_15"
app_title = "Dynamic Css Version 15"
app_publisher = "dynamic business solutions"
app_description = "Dynamic Css version 15"
app_email = "beshoyatef31@gmail.com"
app_license = "mit"
app_logo_url = "/assets/dynamic_15/images/erp-system-logo.png"

# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/dynamic_15/css/dynamic_15.css"
# app_include_js = "/assets/dynamic_15/js/dynamic_15.js"

# include js, css files in header of web template
web_include_css = [
    "/assets/dynamic_15/css/dynamic_15.css",
    "/assets/dynamic_15/css/dynamic_15_login.css"
                   ]
website_context = {
    "favicon": "/assets/dynamic_15/images/new_logo.ico",
    "splash_image": "/assets/dynamic_15/images/erp-system-logo.png"
    }
# web_include_js = "/assets/dynamic_15/js/dynamic_15.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "dynamic_15/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Stock Entry" : "public/js/stock_entry.js",
    "Material Request" : "public/js/material_request.js",
    "Payment Entry" : "public/js/payment_entry.js",
    # "Sales Order" : "public/js/sales_order.js",
    "Sales Invoice" : "public/js/sales_invoice.js",
    "Purchase Order" : "public/js/purchase_order.js",
    "Purchase Invoice" : "public/js/purchase_invoice.js",
    "Task" : "public/js/task.js",
    "Item" : "public/js/item.js",
    "Payment Terms Template": "public/js/payment_terms_template.js",
    "Quotation" : "public/js/quotation.js",
    }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "/assets/dynamic_15/images/dynamic-logo.png"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "dynamic_15.utils.jinja_methods",
# 	"filters": "dynamic_15.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "dynamic_15.install.before_install"
after_install = [
    "dynamic_15.install.after_install",
    ]

after_migrate = [
    "dynamic_15.install.after_install",
]


# Uninstallation
# ------------

# before_uninstall = "dynamic_15.uninstall.before_uninstall"
# after_uninstall = "dynamic_15.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "dynamic_15.utils.before_app_install"
# after_app_install = "dynamic_15.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "dynamic_15.utils.before_app_uninstall"
# after_app_uninstall = "dynamic_15.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "dynamic_15.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# dynamic_15/dynamic_15/hooks.py
override_doctype_class = {
    "Stock Entry": "dynamic_15.override_class.stock_entry.StockEntry"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Payment Entry": {
        "on_update_after_submit": "dynamic_15.api.update_paymentrntry",
    },
    "Journal Entry": {
        "on_submit": "dynamic_15.api.submit_journal_entry",
    },
    "Item": {
        "Item":"dynamic_15.api.create_item_barcode",
    },
    "Sales Order": {
        "on_submit": [
            "dynamic_15.real_state.rs_api.so_on_submit",
        ],
        "before_submit": ["dynamic_15.api.before_submit_so"],
        
    },
    "Stock Ledger Entry": {
        "before_insert": "dynamic_15.real_state.rs_api.stock_ledger_entry_before_insert"
    },
    "Quotation": {
        "before_submit": "dynamic_15.api.before_submit_quot",
        "before_save": "dynamic_15.api.before_save_quotation",
        "on_cancel" :"dynamic_15.api.on_cencel",
    },
    "Stock Entry": {
        "validate": [
            "dynamic_15.api.validate_stock_entry", 
            "dynamic_15.api.check_calculate_weight",  
            # "dynamic_15.api.validat_stock_qty",  
        ],
        "before_insert" :[
            "dynamic_15.api.validat_stock_qty",  

        ]
    },
    "Task": {
        "before_save":[
            "dynamic_15.controllers.before_save",
        ]
    }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"dynamic_15.tasks.all"
# 	],
	"daily": [
 		"dynamic_15.real_state.rs_api.setup_payment_term_notify",
	],
# 	"hourly": [
# 		"dynamic_15.tasks.hourly"
# 	],
# 	"weekly": [
# 		"dynamic_15.tasks.weekly"
# 	],
# 	"monthly": [
# 		"dynamic_15.tasks.monthly"
# 	],
}

# Testing
# -------

# before_tests = "dynamic_15.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "dynamic_15.event.get_events"
# }

#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "dynamic_15.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["dynamic_15.utils.before_request"]
# after_request = ["dynamic_15.utils.after_request"]

# Job Events
# ----------
# before_job = ["dynamic_15.utils.before_job"]
# after_job = ["dynamic_15.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------
override_doctype_dashboards = {
    "Payment Entry": "dynamic_15.public.dashboard.payment_entry_dashboard.get_data",
    "Purchase Invoice": "dynamic_15.public.dashboard.purchase_invoice_dashboard.get_data",
    "Purchase Order": "dynamic_15.public.dashboard.purchase_order_dashboard.get_data",
    "Sales Invoice": "dynamic_15.public.dashboard.sales_invoice_dashboard.get_data",
    "Sales Order": "dynamic_15.public.dashboard.sales_order_dashboard.get_data",
    "Stock Entry": "dynamic_15.public.dashboard.stock_entry_dashboard.get_data",
    "Quotation": "dynamic_15.public.dashboard.quotation_dashboard.get_data",
    "Delivery Note": "dynamic_15.public.dashboard.delivery_note_dashboard.get_data",
    "Task": "dynamic_15.public.dashboard.task_dashboard.get_data",
}


domains = {
    # "Tebian" : "dynamic_15.domains.tebian",
    "Cheques" : "dynamic_15.domains.cheques",
    "Dynamic Accounts" : "dynamic_15.domains.dynamic_accounts",
    "UOM" : "dynamic_15.domains.uom", 
    "Item Barcode":"dynamic_15.domains.item_barcode",
    "POS Subscription":"dynamic_15.domains.pos_subscription",
    "United Enginering" : "dynamic_15.domains.united_engineering",
    "Real State": "dynamic_15.domains.real_state",
}

# auth_hooks = [
# 	"dynamic_15.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
    {
        "dt": ("Custom Field"),
        "filters": [
            [
                "name",
                "in",
                (
                    "Journal Entry Account-party_name",
                    "Cheque-party_name",
                ),
            ]
        ],
    }
]
