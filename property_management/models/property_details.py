# -*- coding: utf-8 -*-

from odoo import fields, models


class PropertyDetails(models.Model):
    _name = 'property.details'
    _description = 'Property Details'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, string='Property')
    address = fields.Text(string='Address')
    image_1920 = fields.Image(max_width=1024, max_height=1024)
    street = fields.Char()
    street2 = fields.Char()
    city = fields.Char()
    zip = fields.Char()
    state_id = fields.Many2one('res.country.state', string="State")
    country_id = fields.Many2one('res.country', string="Country")
    built_date = fields.Date(string='Built Date')
    can_be_sold = fields.Boolean(string='Can Be Sold')
    legal_amount = fields.Integer(string='Legal Amount')
    rent = fields.Integer(string='Rent')
    facility_ids = fields.Many2many('property.facility', string='Facilities')
    state = fields.Selection([
        ('draft', "Draft"),
        ('rented', "Rented"),
        ('Leased', "Leased"),
        ('sold', "Sold")], default='draft', tracking=True)
    description = fields.Html(string='Description')
    owner_id = fields.Many2one('res.partner', string='Owner')
    rent_lease_count = fields.Integer(compute='_compute_count')
    active = fields.Boolean(default=True)
    user_id = fields.Many2one('res.users')

    def get_rental_lease_records(self):
        """ Smart button action to get the rental or lease records for the current property """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rent/Lease',
            'view_mode': 'tree,form',
            'res_model': 'rental.lease.management',
            'domain': [('property_ids.property_id', '=', self.id)],
        }

    def _compute_count(self):
        """To compute the count of records in Rental or Lease Management"""
        for record in self:
            record.rent_lease_count = self.env['rental.lease.management'].search_count(
                [('property_ids.property_id', '=', record.id)])




