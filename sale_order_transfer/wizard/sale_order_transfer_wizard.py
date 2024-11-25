# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import ValidationError


class SaleOrderTransferWizard(models.TransientModel):
        _name = 'sale.order.transfer.wizard'
        _description = 'Sale Order Transfer Wizard'

        warehouse_id = fields.Many2one('stock.warehouse', required=True)

        def action_confirm_transfer(self):
            active_ids = self.env.context.get('active_ids', [])
            order = self.env['sale.order'].browse(active_ids)
            for rec in order:
                if rec.website_id and rec.state == 'sale':
                    rec._action_cancel()
                    rec.action_draft()
                    rec.write({
                        'company_id': self.warehouse_id.company_id.id,
                        'warehouse_id': self.warehouse_id.id,
                        'partner_shipping_id': rec.partner_id.id,
                    })
                    rec.action_confirm()
                else:
                    raise ValidationError("Sale Order Transfer applicable only for Confirmed Sale orders "
                                          "generated through Website!")
