frappe.ui.form.on("Quotation", { 
   
    setup:function(frm) {
        
    },
    
    refresh: function (frm) {  
     
      frm.add_custom_button(
          __("Stock Entry"),
          function () {

          },
          __("Create")
      );
    },
    
    onload: function (frm) {

    },
    
  
    
});
  
  
frappe.ui.form.on("Quotation Item", { 
   
});
  