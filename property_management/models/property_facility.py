# -*- coding: utf-8 -*-

from odoo import models, fields


class Facility(models.Model):
    _name = 'property.facility'
    _description = 'Property Facility'

    name = fields.Char(string="Facility")
