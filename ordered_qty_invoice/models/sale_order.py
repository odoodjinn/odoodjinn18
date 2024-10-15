# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_only_ordered = fields.Boolean(related='partner_id.is_only_ordered')

    def action_testingg(self):
        print(self.env['product.product'].search([('invoice_policy', '=', 'order')]))

    # @api.onchange('order_line.product_id')
    # def onchange_product_id(self):
    #     if self.is_only_ordered:
    #         print('bye')
    #         domain = [('active', '=', False)]
    #         for rec in self.order_line:
    #             if rec.product_id.invoice_policy != 'order':
    #                 print('hi')
    #                 return {'domain': {'product_id': domain}}

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.order_id.is_only_ordered:
            domain = [('active', '!=', True)]
            for rec in self:
                if rec.product_id.invoice_policy != 'order':
                    return {'domain': {'product_id': domain}}