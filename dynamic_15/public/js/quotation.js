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
    get_advancess:function(frm){
      if(!frm.is_return) {
              frappe.call({
          method: "dynamic.api.get_active_domains",
          callback: function (r) {
            if (r.message && r.message.length) {
              if (r.message.includes("Dynamic Accounts")) {
                console.log("Hi");
                return frappe.call({
                  method: "dynamic.ifi.api.get_advance_entries_quotation",//get_advanced_so_ifi
                  args:{
                      doc_name: frm.doc.name,
                  },
                  callback: function(r, rt) {
                    console.log(r.message);
                    frm.clear_table("advancess");
                    let total = 0 ;
                    r.message.forEach(row => {
                      console.log("Hi");
                      console.log(row);
                      let child = frm.add_child("advancess");
                      child.reference_type = row.reference_type,
                      child.reference_name = row.reference_name,
                      child.reference_row = row.reference_row,
                      child.remarks = row.remarks,
                      child.advance_amount = flt(row.amount),
                      child.allocated_amount = row.allocated_amount,
                      child.ref_exchange_rate = flt(row.exchange_rate)
                      total += parseFloat(row.amount);
                    });
                    refresh_field("advancess");
                    frm.set_value("advance_paid" , total);
                    frm.refresh_field("advance_paid");
                    let base_grand_total = parseFloat(frm.doc.grand_total);
                    frm.set_value("outstanding_amount" , base_grand_total - total);
                    frm.refresh_field("base_grand_total");
                  }
                })
              }
          }}
      })
          }
    },
  
    
});
  
  
frappe.ui.form.on("Quotation Item", { 
   
});
  