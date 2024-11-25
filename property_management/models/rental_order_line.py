# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PropertyOrderLine(models.Model):
    _name = 'rental.order.line'
    _description = 'Rental Order Line'

    property_id = fields.Many2one('property.details', string='Property', required=True, ondelete='cascade')
    rental_id = fields.Many2one('rental.lease.management')
    owner_id = fields.Many2one('res.partner', string='Owner', compute='_compute_amount', store=True)
    rent_lease_amount = fields.Integer(string='Rent/Lease Amount', compute='_compute_amount', store=True)
    type = fields.Selection(related='rental_id.type', string='Type')
    start_date = fields.Date(required=True, string='Period')
    end_date = fields.Date(required=True, string='End Date')
    total_days = fields.Float(readonly=True, string='Total Days', store=True, compute='_compute_total_days')
    total_amount = fields.Integer(compute='_compute_total_amount', string='Total Amount')
    invoice_line_ids = fields.One2many('account.move.line', 'line_id')

    @api.depends('rent_lease_amount', 'total_days')
    def _compute_total_amount(self):
        """To calculate the total amount from total days and rent or lease amount per day"""
        for record in self:
            record.total_amount = record.total_days * record.rent_lease_amount

    @api.depends('start_date', 'end_date', 'total_days')
    def _compute_total_days(self):
        """To calculate the total days from start date and end date"""
        for line in self:
            if line.start_date and line.end_date:
                difference = (line.end_date - line.start_date)*24
                line.total_days = int(difference.days)/24

    @api.depends('property_id', 'type')
    def _compute_amount(self):
        """To display the rent or lease amount based on the user selection on Type(selection) field"""
        for rec in self:
            rec.owner_id = rec.property_id.owner_id
            if rec.type == 'rent':
                rec.rent_lease_amount = rec.property_id.rent
            else:
                rec.rent_lease_amount = rec.property_id.legal_amount

    @api.onchange('rent_lease_amount')
    def _onchange_rent_lease_amount(self):
        """Change for rent/lease amount in the order line changes
        the rent and legal amount in property details"""
        if self.type in 'rent':
            self.property_id.rent = self.rent_lease_amount
        else:
            self.property_id.legal_amount = self.rent_lease_amount

