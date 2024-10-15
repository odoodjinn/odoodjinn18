# -*- coding: utf-8 -*-

from odoo import fields, models


class PropertyDetails(models.Model):
    _inherit = 'property.details'

    range_slider = fields.Integer()
