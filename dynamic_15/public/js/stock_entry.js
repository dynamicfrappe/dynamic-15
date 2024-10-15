frappe.ui.form.on('Stock Entry', {
    refresh: function(frm) {
        if(frm.doc.stock_entry_type == "Cuting"){
            frm.set_value("stock_entry_type", "");
            frm.refresh_field("stock_entry_type")
            frm.set_value("stock_entry_type", "Cuting");

        }
    },
});

frappe.ui.form.on('Stock Entry Detail', { 
    item_code: function(frm , cdt , cdn){
        calculate_weight_rate(frm, cdt, cdn);
    },
	qty: function(frm, cdt, cdn) {
        calculate_weight_rate(frm, cdt, cdn);
    },
    weight_per_unit: function(frm, cdt, cdn) {
        calculate_weight_rate(frm, cdt, cdn);
    },
    has_weight: function(frm, cdt, cdn) {
        calculate_total_weight_finished_item(frm, cdt, cdn);
    },
    calculate_weight: function(frm, cdt, cdn) {
        calculate_weight(frm, cdt, cdn);
    },
    is_finished_item: function(frm, cdt, cdn) {
        frappe.call({
            method: "dynamic_15.api.get_active_domains",
            callback: function (r) {
                if (r.message && r.message.length) {
                    if (r.message.includes("Tebian")) {
                        let row = locals[cdt][cdn];
                        if (row.is_finished_item){
                            frappe.model.set_value(cdt, cdn, 'has_weight', 1);
                        }
                        else{
                            frappe.model.set_value(cdt, cdn, 'has_weight', 0);
                        }
                    }
                }
            }
        })
    },
    is_scrap_item: function(frm, cdt, cdn) {
        frappe.call({
            method: "dynamic_15.api.get_active_domains",
            callback: function (r) {
                if (r.message && r.message.length) {
                    if (r.message.includes("Tebian")) {
                        let row = locals[cdt][cdn];
                        if (row.is_scrap_item){
                            frappe.model.set_value(cdt, cdn, 'has_weight', 1);
                        }
                        else{
                            frappe.model.set_value(cdt, cdn, 'has_weight', 0);
                        }
                    }
                }
            }
        })

    },
});

function calculate_weight_rate(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if(row.qty && row.weight_per_unit) {
        frappe.model.set_value(cdt, cdn, 'total_weight', row.qty * row.weight_per_unit);
    }
}

function calculate_total_weight_finished_item(frm , cdt , cdn){
    let row = locals[cdt][cdn];
    let items = frm.doc.items;
    let has_weight = row.has_weight;
    let is_finished_item = row.is_finished_item;
    let qty = row.qty ;
    let sum = 0 ;
    if(has_weight == 1 && is_finished_item == 1){
        const finishedItems = items.filter(item => item.is_finished_item === 0);
        
        for (let i of finishedItems){
            sum += i.total_weight ;
        }

        frappe.model.set_value(cdt, cdn, 'total_weight', sum);
        frappe.model.set_value(cdt, cdn, 'weight_rate', sum / qty);
    }
    let temp = 0 ;
    frappe.db.set_value('Item', row.item_code , 'weight_rate', sum / qty);

}

function calculate_weight(frm, cdt, cdn){
    let row = locals[cdt][cdn];
    if (row.calculate_weight == 1){
        let weight_rate = frm.doc.items[0]['weight_rate'] ; 
        let temp = 0 ;
        if (row.stock_uom == row.uom){
            temp = weight_rate * row.qty ;
        } else {
            temp = weight_rate * row.transfer_qty ;
        }
        frappe.model.set_value(cdt, cdn, 'weight_rate', weight_rate);
        frappe.model.set_value(cdt, cdn, 'total_weight', temp);
    }
    
}    