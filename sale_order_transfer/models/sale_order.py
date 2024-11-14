# -*- coding: utf-8 -*-

from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_transfer_so(self):
        active_ids = self.env.context.get('active_ids')
        if active_ids:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Sale Order Transfer Wizard',
                'res_model': 'sale.order.transfer.wizard',
                'view_mode': 'form',
                'target': 'new',
            }
    def hello(self):
        print('helloooo')

