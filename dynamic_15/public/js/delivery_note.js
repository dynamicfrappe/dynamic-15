frappe.ui.form.on("Delivery Note", { 
   
    setup:function(frm) {
        
    },
    
    refresh: function (frm) {  
     
      frm.add_custom_button(
          __("Task"),
          function () {

          },
          __("Create")
      );
    },
    
    onload: function (frm) {

    },
    
  
    
});
  
  
frappe.ui.form.on("Delivery Note Item", { 
   
});
  