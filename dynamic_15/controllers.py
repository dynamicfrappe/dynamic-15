
import frappe

from frappe import _

domains = frappe.get_active_domains()

def before_save(doc, method):
    
    if "United Enginering" in frappe.get_active_domains():

        l = []  # List to store the previous tasks
        for dependent_task in doc.depends_on:
            dep_task_doc = frappe.get_doc('Task', dependent_task.task)
            
            for task in l:
                exists = any(dep.task == task for dep in dep_task_doc.depends_on)
                if not exists:
                    dep_task_doc.append('depends_on', {
                        'task': task
                    })

            dep_task_doc.save()
            l.append(dependent_task.task)

        if doc.status != 'Pending' and is_blocked(doc.name):
            frappe.throw(_("You cannot open this task until the previous tasks are completed or cancelled."))

def is_blocked(task):
    task = frappe.get_doc("Task", task)
    if task.depends_on:
        for dep in task.depends_on:
            dep_task = frappe.get_doc('Task', dep.task)
            if dep_task.status != 'Completed' or dep_task.status != 'Cancelled' :
                return True

    return False