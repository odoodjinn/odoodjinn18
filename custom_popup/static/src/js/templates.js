/**@odoo-module **/
import { Dialog } from "@web/core/dialog/dialog";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { Component } from "@odoo/owl";


class customPopupTemplate extends Component {
   static template = "custom_popup.customPopupTemplate";
   static components = { Dialog };
}

patch(ControlButtons.prototype, {
    customPopup(){
        console.log('hi')
        this.dialog.add(customPopupTemplate, {
        title: 'Title',
        body: 'popup'
        })
    }
})
