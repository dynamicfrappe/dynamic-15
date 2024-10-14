frappe.ui.form.on("Material Request", { 
    refresh: function(frm) {
        if(frm.doc.docstatus == 1 && (frm.doc.material_request_type == "Manufacture" || frm.doc.material_request_type == "Cuting")){            
            frm.add_custom_button(
                __("Stock Entry"),
                function () {
                    frappe.model.open_mapped_doc({
                        method:"dynamic_15.api.create_stock_entry",
                        frm: frm,
                      });
                },
                __("Create")
            );

        }
    },
});

  