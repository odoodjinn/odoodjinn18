/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { useService } from "@web/core/utils/hooks";


publicWidget.registry.rental_lease_web_form = publicWidget.Widget.extend({
    selector: '#rental_lease_web_form_template',
    events: {
    'click .custom_create': '_onClickSubmit',
    'click .add_line': '_onClickAdd_line',
    'click .remove_line': '_onClickRemove_line',
    },
    setup(){
        super.setup()
        this.orm = useService('orm')
    }

_onClickSubmit: async function(ev){
    var order_line_list = [];
    var rows = $(ev.currentTarget).parent().prev().prev().find('.order_line');
    var tenant_id = $(ev.currentTarget).parent().prev().prev().prev().find('select[name="tenant_id"]').val();
    var due_date = $(ev.currentTarget).parent().prev().prev().prev().find('input[name="due_date"]').val();
    var company_id = $(ev.currentTarget).parent().prev().prev().prev().find('select[name="company_id"]').val();
    var type = $(ev.currentTarget).parent().prev().prev().prev().find('select[name="type"]').val();
    var check = 0;
    if(tenant_id==""){
        alert('Tenant name is mandatory!!')
    }
    else if(due_date==""){
        alert('Due Date is mandatory!!')
    }
    else{
        $.each(rows, function(row) {
            let property_id = $(this).find('select[name="property_id"]').val();
            let start_date = $(this).find('input[name="start_date"]').val();
            let end_date = $(this).find('input[name="end_date"]').val();
            if (property_id == ""){
                check = 0
                alert('Property field is mandatory!!!!')
            }else if (start_date == ""){
                check = 0
                alert('Start Date is mandatory!!')
            }else if (end_date == ""){
                check = 0
                alert('End Date is mandatory!!')
            }else if (start_date>end_date){
                check = 0
                alert("Invalid Date Range!\nStart Date cannot be after End Date!")
            }else{
                check = 1
                order_line_list.push({
                    'property_id': property_id,
                    'start_date': start_date,
                    'end_date': end_date,
                });
            }
//            var values = {
//                'tenant_id': tenant_id,
//                'due_date': due_date,
//                'company_id': company_id,
//                'type': type,
//            }
        });
        if (check==1){
//            await this.orm.create("rental.lease.management",[values] )
            jsonrpc('/management/submit', {order_line_list, tenant_id, due_date, company_id, type}).then((res)=>{
                window.location.href = "/contactus-thank-you"
            });
            }
    }
},
_onClickRemove_line: function(ev){
    var targetElement = ev.target.closest('.order_line')
    $(targetElement).remove();
},
_onClickAdd_line: function(ev){
    var new_row = $(ev.currentTarget).parent().prev().find('.add_extra_order_line').clone();
    new_row.removeClass('d-none');
    new_row.removeClass('add_extra_order_line');
    new_row.addClass('order_line');
    new_row.insertBefore($('.add_extra_order_line'));
},
});
