frappe.ui.form.on("Payment Entry", {
  
    paid_from:function(frm) {
      frm.doc.currency_exchange =1
      frm.set_df_property("currency_exchange" , "hidden" , 1) 
      var account = frm.doc.paid_from 
      var currency = frm.doc.paid_from_account_currency 
      if (currency != frappe.get_doc(":Company", frm.doc.company).default_currency ) {
        frappe.call({
          "method" :"dynamic_15.dynamic_15.utils.currency_valuation_rate" ,
           async: false,
          "args" :{
            "account" : account
          },callback :function(r){
           if (r.message) {
            frm.doc.currency_exchange = r.message
            frm.set_df_property("currency_exchange" , "hidden" , 0) 
            frm.refresh_field("currency_exchange")
           }
          }
        })
      }
    },

    refresh(frm) {
        console.log(frm.doc.docstatus)
        // your code here
        if (frm.doc.docstatus == 1 && frm.doc.cheque) {
          frm.events.add_cheque_buttons(frm);
        }
        console.log(frm.doc.cheque)
        if(frm.doc.is_from_cheque_submission){
          frm.set_df_property("cheque" , "hidden" , 0) 
          frm.set_df_property("cheque_status" , "hidden" , 0) 
          frm.set_df_property("endorse_cheque" , "hidden" , 0)
        }
        if(frm.doc.cheque_status == "Under Collect"){
          frm.set_df_property("cash_mod_of_payment" , "hidden" , 0)
        }
        else{
          frm.set_df_property("cash_mod_of_payment" , "hidden" , 1)
        }
     },
    add_cheque_buttons(frm) {
      if (frm.doc.payment_type == "Pay" && frm.doc.cheque_status == "New") {
        frm.add_custom_button(
          __("Pay"),
          function () {
            // frm.events.add_row_cheque_tracks(frm,'Paid')
            frm.events.make_cheque_pay(frm);
          },
          __("Cheque Management")
        );
        //** replace cheque by cash */
        frm.add_custom_button(
          __("Cash"),
          function(){
            frm.events.pay_cash_new(frm)
          },
          __("Cheque Management")
        );
        
      }
      if (frm.doc.payment_type == "Receive") {
        if (["New"].includes(frm.doc.cheque_status)) {
          // cheque Endorsement
          frm.add_custom_button(
            __("Endorsement"),
            function () {
              frm.events.make_cheque_endorsement(frm);
            },
            __("Cheque Management")
          );
          // Collections Cheque Now
          frm.add_custom_button(
            __("Collect Now"),
            function () {
              frm.events.collect_cheque_now(frm);
            },
            __("Cheque Management")
          );
          // deposite Cheque under collcttion
          frm.add_custom_button(
            __("Deposit Under Collection"),
            function () {
              frm.events.deposite_cheque_under_collection(frm);
            },
            __("Cheque Management")
          );
        }
        if (["New"].includes(frm.doc.cheque_status)) {
        }
  
        // cheque under collction
  
        if (["Under Collect"].includes(frm.doc.cheque_status)) {
          frm.add_custom_button(
            __("Collect"),
            function () {
              frm.events.collect_cheque_under_collection(frm);
            },
            __("Cheque Under Collection")
          );
          //** replace cheque by cash */
          frm.add_custom_button(
            __("Cash"),
            function(){
              frm.events.pay_cash_new(frm)
            },
            __("Cheque Under Collection")
          );
          frm.add_custom_button(
            __("Reject"),
            function () {
              frm.events.reject_cheque_under_collection(frm);
            },
            __("Cheque Under Collection")
          );
          frm.add_custom_button(
            __("Reject Cheque In Bank"),
            function () {
              frm.events.add_row_cheque_tracks(frm,"Rejected In Bank")
            },
            __("Cheque Under Collection")
          );
          // return_cheque_xx
          frm.add_custom_button(
            __("Return Cheque"),
            function () {
              frm.events.return_cheque(frm);
            },
            __("Cheque Under Collection")
          );
        }
  
        // Reject cheque under collction
        if (["Rejected in Bank"].includes(frm.doc.cheque_status)) {
          // deposite Cheque under collcttion
          frm.add_custom_button(
            __("Deposit Under Collection"),
            function () {
              frm.events.deposite_cheque_under_collection(frm);
            },
            __("Cheque Management")
          );
        }
  
        
      }
    },
    make_cheque_endorsement(frm) {
      if (!frm.doc.drawn_bank_account) {
        frappe.throw(__("Please Set Bank Account"));
      }
      frappe.call({
        method: "dynamic_15.cheques.doctype.cheque.cheque.make_cheque_endorsement",
        args: {
          payment_entry: frm.doc.name,
        },
        callback: function (r) {
          frm.refresh();
          if (r && r.message) {
            frappe.set_route("Form", r.message.doctype, r.message.name);
          }
        },
      });
    },
    collect_cheque_now(frm) {
      frappe.call({
        method: "dynamic_15.cheques.doctype.cheque.cheque.collect_cheque_now",
        args: {
          payment_entry: frm.doc.name,
        },
        callback: function (r) {
          frm.refresh();
          if (r && r.message) {
            frappe.set_route("Form", r.message.doctype, r.message.name);
          }
        },
      });
    },
    deposite_cheque_under_collection(frm) {
      frappe.call({
        method:
          "dynamic_15.cheques.doctype.cheque.cheque.deposite_cheque_under_collection",
        args: {
          payment_entry: frm.doc.name,
        },
        callback: function (r) {
          frm.refresh();
          if (r && r.message) {
            frappe.set_route("Form", r.message.doctype, r.message.name);
          }
        },
      });
    },
    return_cheque(frm) {
      frappe.call({
        method:
          "dynamic_15.cheques.doctype.cheque.cheque.return_cheque",
        args: {
          payment_entry: frm.doc.name,
        },
        callback: function (r) {
          // frm.refresh();
          if (r && r.message) {
            frappe.set_route("Form", r.message.doctype, r.message.name);
          }
        },
      });
    },
    collect_cheque_under_collection(frm) {
      frappe.call({
        method:
          "dynamic_15.cheques.doctype.cheque.cheque.collect_cheque_under_collection",
        args: {
          payment_entry: frm.doc.name,
        },
        callback: function (r) {
          frm.refresh();
          if (r && r.message) {
            frappe.set_route("Form", r.message.doctype, r.message.name);
          }
        },
      });
    },
    reject_cheque_under_collection(frm) {
      frappe.call({
        method:
          "dynamic_15.cheques.doctype.cheque.cheque.reject_cheque_under_collection",
        args: {
          payment_entry: frm.doc.name,
        },
        callback: function (r) {
          frm.refresh();
          if (r && r.message) {
            frappe.set_route("Form", r.message.doctype, r.message.name);
          }
        },
      });
    },
    make_cheque_pay(frm) {
      if (!frm.doc.drawn_bank_account) {
        frappe.throw(__("Please Set Bank Account"));
      }
      frappe.call({
        method: "dynamic_15.cheques.doctype.cheque.cheque.make_cheque_pay",
        args: {
          payment_entry: frm.doc.name,
        },
        callback: function (r) {
          frm.refresh();
          if (r && r.message) {
            frappe.set_route("Form", r.message.doctype, r.message.name);
          }
        },
      });
    },
    add_row_cheque_tracks(frm,new_cheque_status) {
      // if (!frm.doc.drawn_bank_account) {
      //   frappe.throw(__("Please Set Bank Account"));
      // }
      frappe.call({
        method:"dynamic_15.cheques.doctype.cheque.cheque.add_row_cheque_tracks",
        args:{
          payment_entry:frm.doc.name,
          new_cheque_status:new_cheque_status
        },
        callback:function(r){
          if(!r.exc){
            frm.refresh()
          }else{
            frappe.throw(r.exc)
          }
        }
      })
    },
    pay_cash_new(frm){
      if (!frm.doc.cash_mod_of_payment) {
        frappe.throw(__("Please Add Cash Mode Of Payment"));
      }
      frappe.call({
        method:"dynamic_15.cheques.doctype.cheque.cheque.pay_cash_new",
        args:{
          payment_entry : frm.doc.name,
        },
        callback:function(r){
          if(!r.exc){
            frm.refresh()
            frappe.set_route("Form", r.message.doctype, r.message.name);
          }else{
            frappe.throw(r.exc)
          }
        }
      })
    }
  });
  