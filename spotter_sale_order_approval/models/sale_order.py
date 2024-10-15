# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('to_approve', 'To Approve'),
                                            ('secondary_approval', 'Secondary Approval'),
                                            ('sent',)])
    primary_user_id = fields.Many2one('res.users', compute='_compute_user')
    secondary_user_id = fields.Many2one('res.users', compute='_compute_user')
    primary_val = fields.Char(compute='_compute_val')
    secondary_val = fields.Char(compute='_compute_val')

    def _compute_user(self):
        """ function definition to fetch the approval users field from settings"""
        user_check = self.env['res.config.settings'].sudo().search([])
        for rec in user_check:
            for record in self:
                record.primary_user_id = rec.primary_user_id
                record.secondary_user_id = rec.secondary_user_id

    @api.depends('primary_user_id', 'secondary_user_id')
    def _compute_val(self):
        """Function to show approval buttons only to the users selected in the settings"""
        uid = self.env.user
        for rec in self:
            if rec.primary_user_id == uid:
                rec.primary_val = '1'
            else:
                rec.primary_val = '0'
            if rec.secondary_user_id == uid:
                rec.secondary_val = '1'
            else:
                rec.secondary_val = '0'


    def _can_be_confirmed(self):
        self.ensure_one()
        return self.state in {'draft', 'sent', 'secondary_approval'}

    def _confirmation_error_message(self):
        """ Return whether order can be confirmed or not if not then returm error message. """
        self.ensure_one()
        if self.state not in {'draft', 'sent', 'secondary_approval'}:
            return _("Some orders are not in a state requiring confirmation.")
        if any(
                not line.display_type
                and not line.is_downpayment
                and not line.product_id
                for line in self.order_line
        ):
            return _("A line on these orders missing a product, you cannot confirm it.")

        return False
    def action_confirm(self):
        """Confirm button action to check if the total SO amount is more than 25000,
        if the condition is true it changes the SO state to 'to approve'.
        Otherwise, it will create SO directly.
        """
        if (self.amount_total > 25000) and (self.state not in ['to_approve', 'secondary_approval']):
            self.state = 'to_approve'
            return
        return super(SaleOrder, self).action_confirm()

    def action_approve(self):
        """Primary approve button to change the state to secondary approval"""
        self.state = 'secondary_approval'

    def action_second_approve(self):
        """Secondary approve button to confirm the SO"""
        self.action_confirm()