// Copyright (c) 2024, dynamic business solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Real Estate Sittings', {
	refresh: function(frm) {
		frm.add_custom_button(__("Check Alert"),()=>{
			frm.call({
				method:"dynamic_15.real_state.rs_api.setup_payment_term_notify",
				callbcak:function(r){
					console.log('succcess')
				}
			})
		})

	}
});
