frappe.ui.form.on("Sales Invoice", {
    setup(frm) {
      frappe.call({
        method: "dynamic_15.api.get_active_domains",
        callback: function (r) {
          if (r.message && r.message.length) {
            if (r.message.includes("Cheques")) {
                frm.custom_make_buttons["Cheque"] = "Cheque";
            }
            }
        }
     })
    },
    refresh(frm) {
      frm.events.add_cheque_button(frm);
      frm.events.set_query(frm)


    },

    add_cheque_button(frm) {
      if (frm.doc.docstatus == 1) {
        frappe.call({
          method: "dynamic_15.api.get_active_domains",
          callback: function (r) {
            if (r.message && r.message.length) {
              if (r.message.includes("Cheques")) {
                if (
                  frm.doc.outstanding_amount != 0 &&
                  !(cint(frm.doc.is_return) && frm.doc.return_against)
                ) {
                  frm.add_custom_button(
                    __("Cheque"),
                    function () {
                      frm.events.make_cheque_doc(frm);
                    },
                    __("Create")
                  );
                }
              }
            }
          },
        });
      }
    },
    make_cheque_doc(frm) {
      return frappe.call({
        method: "dynamic_15.cheques.doctype.cheque.cheque.make_cheque_doc",
        args: {
          dt: frm.doc.doctype,
          dn: frm.doc.name,
        },
        callback: function (r) {
          var doc = frappe.model.sync(r.message);
          frappe.set_route("Form", doc[0].doctype, doc[0].name);
        },
      });
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
  
  
  frappe.ui.form.on("Sales Invoice Item", {
  
  })