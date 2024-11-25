# -*- coding: utf-8 -*-

from odoo import fields, models


class Owner(models.Model):
    _inherit = 'res.partner'

    owned_properties = fields.One2many('property.details', 'owner_id', string='Owned Properties')

