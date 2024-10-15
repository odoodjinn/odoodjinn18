# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
   _inherit = 'res.config.settings'

   primary_user_id = fields.Many2one(comodel_name='res.users', string='Primary Approval User',
         config_parameter='spotter_sale_order_approval.primary_user',
         help='Primary approval person for the SO above 25K ')
   secondary_user_id = fields.Many2one(comodel_name='res.users', string='Secondary Approval User',
         config_parameter='spotter_sale_order_approval.secondary_user',
         help='Secondary approval person for the SO above 25K ')
