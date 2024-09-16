frappe.ui.form.on("Task",{
    setup:function(frm) {
        
    },
    
    refresh: function (frm) {
        frm.set_value("description", frm.doc.attach_pdf)
        
    },
    
    onload: function (frm) {

    },    
  
    
});
