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
                    raise ValidationError("Sale Order Transfer applicable only for Confirmed Sale orders generated "
                                          "through Website!")


            # for rec in active_ids:
            # record = self.env['sale.order'].search([
            #     ('id', '=', rec),
            #     ('website_id', '!=', False),
            #     ('state', '=', 'sale')
            # ])
            # if record:
            # old_delivery = record.picking_ids
            # if old_delivery:
            #     old_delivery.action_cancel()
            # new_picking = self.env['stock.picking'].create([{
            #     'company_id': self.warehouse_id.company_id.id,
            #     'partner_id': record.partner_id.id,
            #     'origin': record.name,
            #     'move_type': 'direct',
            #     'picking_type_id': self.warehouse_id.out_type_id.id,
            #     'scheduled_date': fields.Date.today(),
            #     'sale_id': record.id,
            #     'state': 'draft',
            # }])

            # for line in record.order_line:
            #     self.env['stock.move'].create([{
            #         'name': line.product_id.name,
            #         'product_id': line.product_id.id,
            #         'product_uom': line.product_uom.id,
            #         'product_uom_qty': line.product_uom_qty,
            #         'picking_id': new_picking.id,
            #         'state': 'draft',
            #         'company_id': self.warehouse_id.company_id.id,
            #         'location_id': new_picking.location_id.id,
            #         'location_dest_id': new_picking.location_dest_id.id,
            #     }])
            # new_picking.action_confirm()

            # record.order_line.write({
            #     'company_id': self.warehouse_id.company_id.id,
            # })
            # record.sudo().write({
            #     'warehouse_id': self.warehouse_id.id,
            #     'company_id': self.warehouse_id.company_id.id,
            #     'partner_shipping_id': record.partner_id.id,
            # })
            # else:
            #     raise ValidationError("Sale Order Transfer applicable only for Confirmed Sale orders generated "
            #                           "through Website!")
