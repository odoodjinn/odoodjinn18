# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    rental_lease_id = fields.Many2one('rental.lease.management', string='Rental/Lease')


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    line_id = fields.Many2one('rental.order.line', string='Invoice Line')

