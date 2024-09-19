
from frappe import _
from frappe import get_active_domains

DOMAINS = get_active_domains()


def get_data(data={}):
    dashboard_data = data
    if "United Enginering" in DOMAINS:
        dashboard_data["transactions"].append(
            {
                'label': _('References'),
                'items': ['Stock Entry']
            },
        )

    return dashboard_data
