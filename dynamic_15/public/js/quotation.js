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

      frm.events.set_query(frm)
    },
    
    onload: function (frm) {

    },
    
    set_query:function(frm){
      frappe.call({
          method: "dynamic_15.api.get_active_domains",
          callback: function (r) {
            if (r.message && r.message.length) {
              if (r.message.includes("Real State")) {
                frm.set_query('item_code', 'items', function(doc, cdt, cdn) {
                  return {
                    filters:{"reserved":0}
                  };
                });
              }
          }}
      })
  },
  
    
});
  
  
frappe.ui.form.on("Quotation Item", { 
   
});
  