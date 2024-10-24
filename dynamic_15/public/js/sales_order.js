
frappe.ui.form.on("Sales Order", { 
   
    setup:function(frm) {
      frm.custom_make_buttons = {
        "Cheque": "Cheque",
      };
      // frm.events.setup_doc_event(frm)
    },

    refresh: function (frm) {  
     
      // frm.events.add_cheque_button(frm);

    },
    
    onload: function (frm) {
    },
    
    transaction_date:function(frm){
      // frm.events.setup_doc_event(frm)
    },
    
    setup_doc_event:function(frm){
      if (frm.doc.transaction_date){
        frappe.call({
          method: "dynamic_15.api.get_active_domains",
          callback: function (r) {
            if (r.message && r.message.length) {
              if (r.message.includes("Real State")) {
                frappe.call({
                  method:"dynamic_15.real_state.rs_api.add_year_date",
                  args:{
                    trans_date:  frm.doc.transaction_date
                    },
                  callback:function(r){
                    frm.set_value('delivery_date',r.message)
                    frm.refresh_field('delivery_date')
                  }
                })
              }
          }}
      })
      }
    },
    get_advancess:function(frm){
      if(!frm.is_return) {
        frappe.call({
          method: "dynamic_15.api.get_active_domains",
          callback: function (r) {
            if (r.message && r.message.length) {
              if ( r.message.includes("Dynamic Accounts")) {
                return frappe.call({
                  method: "dynamic_15.api.get_advanced_so_ifi",
                  args:{
                    doc_name: frm.doc.name,
                  },
                  callback: function(r, rt) {
                    frm.clear_table("advancess");
                    r.message.forEach(row => {
                      // console.log(row)
                      let child = frm.add_child("advancess");
                      child.reference_type = row.reference_type,
                      child.reference_name = row.reference_name,
                      child.reference_row = row.reference_row,
                      child.remarks = row.remarks,
                      child.advance_amount = flt(row.amount),
                      child.allocated_amount = row.allocated_amount,
                      child.ref_exchange_rate = flt(row.exchange_rate)
                    });
                    refresh_field("advancess");
                  }
                })
              }
          }}
      })
      }
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
    
    set_warehouse: function (frm) {
      frm.events.autofill_warehouse(
        frm,
        frm.doc.items,
        "item_warehouse",
        frm.doc.set_warehouse
      );
    },
    purchase_order: function (frm) {
      frm.events.autofill_purchase_order(
        frm,
        frm.doc.items,
        "item_purchase_order",
        frm.doc.purchase_order
      );
    },
    autofill_warehouse: function (frm, child_table, warehouse_field, warehouse) {
      if (warehouse && child_table && child_table.length) {
        let doctype = child_table[0].doctype;
        $.each(child_table || [], function (i, item) {
          frappe.model.set_value(doctype, item.name, warehouse_field, warehouse);
        });
      }
    },
    autofill_purchase_order: function (
      frm,
      child_table,
      warehouse_field,
      warehouse
    ) {
      if (warehouse && child_table && child_table.length) {
        let doctype = child_table[0].doctype;
        $.each(child_table || [], function (i, item) {
          frappe.model.set_value(doctype, item.name, warehouse_field, warehouse);
        });
      }
    },
  
    
   
  update_child_items : function(frm,child_docname,child_doctype,cannot_add_row) {
      var cannot_add_row = (typeof cannot_add_row === 'undefined') ? true : cannot_add_row;
      var child_docname = (typeof cannot_add_row === 'undefined') ? "items" : child_docname;
      var child_meta = frappe.get_meta(`${frm.doc.doctype} Item`);
  
      const get_precision = (fieldname) => child_meta.fields.find(f => f.fieldname == fieldname).precision;
  
      this.data = [];
      const fields = [{
          fieldtype:'Data',
          fieldname:"docname",
          read_only: 1,
          hidden: 1,
      }, {
          fieldtype:'Link',
          fieldname:"item_code",
          options: 'Item',
          in_list_view: 1,
          read_only: 0,
          disabled: 0,
          label: __('Item Code'),
          get_query: function() {
              let filters;
              if (frm.doc.doctype == 'Sales Order') {
                  filters = {"is_sales_item": 1};
              } else if (frm.doc.doctype == 'Purchase Order') {
                  if (frm.doc.is_subcontracted == "Yes") {
                      filters = {"is_sub_contracted_item": 1};
                  } else {
                      filters = {"is_purchase_item": 1};
                  }
              }
              return {
                  query: "erpnext.controllers.queries.item_query",
                  filters: filters
              };
          }
      }, {
          fieldtype:'Link',
          fieldname:'uom',
          options: 'UOM',
          read_only: 0,
          label: __('UOM'),
          reqd: 1,
          onchange: function () {
              frappe.call({
                  method: "erpnext.stock.get_item_details.get_conversion_factor",
                  args: { item_code: this.doc.item_code, uom: this.value },
                  callback: r => {
                      if(!r.exc) {
                          if (this.doc.conversion_factor == r.message.conversion_factor) return;
  
                          const docname = this.doc.docname;
                          dialog.fields_dict.trans_items.df.data.some(doc => {
                              if (doc.docname == docname) {
                                  doc.conversion_factor = r.message.conversion_factor;
                                  dialog.fields_dict.trans_items.grid.refresh();
                                  return true;
                              }
                          })
                      }
                  }
              });
          }
      }, {
          fieldtype:'Float',
          fieldname:"qty",
          default: 0,
          read_only: 0,
          in_list_view: 1,
          label: __('Qty'),
          precision: get_precision("qty")
      }, {
          fieldtype:'Currency',
          fieldname:"rate",
          options: "currency",
          default: 0,
          read_only: 0,
          in_list_view: 1,
          label: __('Rate'),
          precision: get_precision("rate")
      }];
  
      if (frm.doc.doctype == 'Sales Order' || frm.doc.doctype == 'Purchase Order' ) {
          fields.splice(2, 0, {
              fieldtype: 'Date',
              fieldname: frm.doc.doctype == 'Sales Order' ? "delivery_date" : "schedule_date",
              in_list_view: 1,
              label: frm.doc.doctype == 'Sales Order' ? __("Delivery Date") : __("Reqd by date"),
              reqd: 1
          })
          fields.splice(3, 0, {
              fieldtype: 'Float',
              fieldname: "conversion_factor",
              in_list_view: 1,
              label: __("Conversion Factor"),
              precision: get_precision('conversion_factor')
          })
      }
  
      const dialog = new frappe.ui.Dialog({
          title: __("Update Items"),
          fields: [
              {
                  fieldname: "trans_items",
                  fieldtype: "Table",
                  label: "Items",
                  cannot_add_rows: cannot_add_row,
                  in_place_edit: false,
                  reqd: 1,
                  data: this.data,
                  get_data: () => {
                      return this.data;
                  },
                  fields: fields
              },
          ],
          primary_action: function() {
              const trans_items = this.get_values()["trans_items"].filter((item) => !!item.item_code);
              frappe.call({
                  method: 'erpnext.controllers.accounts_controller.update_child_qty_rate',
                  freeze: true,
                  args: {
                      'parent_doctype': frm.doc.doctype,
                      'trans_items': trans_items,
                      'parent_doctype_name': frm.doc.name,
                      'child_docname': child_docname
                  },
                  callback: function() {
                      frm.reload_doc();
                  }
              });
              this.hide();
              refresh_field("items");
          },
          primary_action_label: __('Update')
      });
  
      frm.doc[child_docname].forEach(d => {
          dialog.fields_dict.trans_items.df.data.push({
              "docname": d.name,
              "name": d.name,
              "item_code": d.item_code,
              "delivery_date": d.delivery_date,
              "schedule_date": d.schedule_date,
              "conversion_factor": d.conversion_factor,
              "qty": d.qty,
              "rate": d.rate,
              "uom": d.uom
          });
          this.data = dialog.fields_dict.trans_items.df.data;
          dialog.fields_dict.trans_items.grid.refresh();
      })
      dialog.show();
  },
  
  });
  
  erpnext.selling.SalesOrderController = class SalesOrderController extends erpnext.selling.SellingController {
    
     refresh(doc, dt, dn)  {
      var me = this;
      this._super(doc);
        if(doc.status !== 'Closed') {
          if(doc.status !== 'On Hold') {
            
            frappe.call({
              method: "dynamic_15.api.get_active_domains",
              callback: function (r) {
                if (r.message && r.message.length) {
                  
                  if (r.message.includes("Real State")){
                    // console.log('domains real state')
                    cur_frm.cscript['get_method_for_payment'] = create_payment_for_real_state
                  }
                }
              }
            })
  
          }
        }
    }
    
  };
  
  var create_payment_for_real_state = function(){
    var method = "dynamic_15.real_state.rs_api.get_payment_entry";
    if(cur_frm.doc.__onload && cur_frm.doc.__onload.make_payment_via_journal_entry){
      if(in_list(['Sales Invoice', 'Purchase Invoice'],  cur_frm.doc.doctype)){
        method = "erpnext.accounts.doctype.journal_entry.journal_entry.get_payment_entry_against_invoice";
      }else {
        method= "erpnext.accounts.doctype.journal_entry.journal_entry.get_payment_entry_against_order";
      }
    }
    // console.log(method)
    return method
  }

  extend_cscript(cur_frm.cscript, new erpnext.selling.SalesOrderController({ frm: cur_frm }));
  // $.extend(
  // 	cur_frm.cscript,
  // 	new extend_sales_order({frm: cur_frm}),
  // );

  frappe.ui.form.on("Sales Order Item", { 
   
  });
  