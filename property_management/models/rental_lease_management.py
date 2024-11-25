# -*- coding: utf-8 -*-

from odoo import api, Command, fields, models
from odoo.exceptions import ValidationError


class RentalLeaseManagement(models.Model):
    _name = 'rental.lease.management'
    _description = 'Rental/Lease Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(readonly=True, string='Sequence')
    property_ids = fields.One2many('rental.order.line', 'rental_id', string="Order Lines")
    type = fields.Selection([('rent', 'Rent'), ('lease', 'Lease')], default='rent', string='Type')
    due_date = fields.Date(string='Due Date', required=True)
    tenant_id = fields.Many2one('res.partner', required=True, string='Tenant')
    company_id = fields.Many2one(comodel_name='res.company', readonly=True,
                                 default=lambda self: self.env.company, string='Company')
    state = fields.Selection([('to_approve', 'To Approve'), ('draft', 'Draft'), ('confirmed', 'Confirmed'),
                              ('closed', 'Closed'), ('returned', 'Returned'), ('expired', 'Expired')],
                             default='to_approve', tracking=True, string='Status')
    invoice_count = fields.Integer(compute='_compute_invoice_count')
    invoice_ids = fields.One2many('account.move', 'rental_lease_id', string='Invoices')
    payment_state = fields.Selection([('paid', 'Paid'), ('partial', 'Partial'), ('not_paid', 'Not Paid'),
                                      ('no_invoice', 'No Invoice')], compute='_compute_payment_state')

    @api.depends('invoice_ids.payment_state')
    def _compute_payment_state(self):
        """Display ribbon in rental/lease order based on the invoice payment status"""
        for rec in self:
            paid_invoice = self.invoice_ids.filtered(lambda inv: inv.payment_state == 'paid')
            not_paid_invoice = self.invoice_ids.filtered(lambda x: x.payment_state != 'paid')
            if rec.invoice_ids:
                if paid_invoice and not_paid_invoice:
                    rec.payment_state = 'partial'
                elif paid_invoice:
                    rec.payment_state = 'paid'
                else:
                    rec.payment_state = 'not_paid'
            else:
                rec.payment_state = "no_invoice"

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        """To show the count of Invoices in smart button"""
        for record in self:
            record.invoice_count = len(record.invoice_ids)

    def get_invoice_records(self):
        """ Smart button action to get the invoice records for the current rent or lease record """
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.invoice_ids.ids)],
        }

    @api.model_create_multi
    def create(self, vals_list):
        """Function to create sequence numbers for Rental or Lease records"""
        sequences = super().create(vals_list)
        for rec in sequences:
            rec['name'] = self.env['ir.sequence'].next_by_code('rental_sequence_code')
        return sequences

    # === ACTION METHODS ===#

    def action_approve(self):
        """Button to approve the rental/lease order requests from user"""
        self.state = 'draft'

    def action_confirm(self):
        """Function to set the attachment as mandatory on confirm button and change the state to Confirmed"""
        attachments = self.env['ir.attachment'].search([('res_model', '=', self._name),
                                                        ('res_id', '=', self.id)])
        if not attachments:
            raise ValidationError("Attach a file to confirm")
        else:
            template = self.env.ref('property_management.email_template_confirmed')
            template.send_mail(self.id, force_send=True)
            self.state = 'confirmed'

    def action_close(self):
        """Action on Close button to change the state to Closed"""
        template = self.env.ref('property_management.email_template_closed')
        template.send_mail(self.id, force_send=True)
        self.state = 'closed'

    def action_return(self):
        """Action on Return button to change the state to Returned"""
        self.state = 'returned'

    def action_expired(self):
        """Action on Expired button to change the state to Expired"""
        template = self.env.ref('property_management.email_template_expired')
        template.send_mail(self.id, force_send=True)
        self.state = 'expired'

    def action_draft(self):
        """Action on Reset to draft button to change the state to Draft"""
        self.state = 'draft'

    def action_create_invoice(self):
        """Button action to perform invoice generation from rental/lease order"""
        if self.invoice_ids:
            posted_invoice = self.invoice_ids.filtered(lambda inv: inv.state == 'posted')
            draft_invoice = self.invoice_ids.filtered(lambda inv: inv.state == 'draft')
            if draft_invoice:
                lines = []
                for rec in self.property_ids:
                    if ((rec.id not in posted_invoice.invoice_line_ids.line_id.ids) and
                            (rec.id in posted_invoice.invoice_line_ids.line_id.ids)):
                        invoice_line_values = {
                            'name': rec.property_id.name,
                            'price_unit': rec.rent_lease_amount,
                            'price_subtotal': rec.total_amount,
                            'quantity': rec.total_days,
                            'line_id': rec.id
                        }
                        lines.append(Command.create(invoice_line_values))
                for record in draft_invoice:
                    record.write({'invoice_line_ids': lines})
                    return {
                        'type': 'ir.actions.act_window',
                        'res_model': 'account.move',
                        'view_type': 'tree,form',
                        'view_mode': 'form',
                        'res_id': record.id,
                        'view_id': (self.env.ref('account.view_move_form').id, 'form'),
                    }
            else:
                # posted invoice
                lines = []
                for rec in self.property_ids:
                    for line in posted_invoice.invoice_line_ids:
                        difference_qty = rec.total_days - line.quantity
                        difference_amount = line.price_unit * line.quantity
                        if rec.id in line.line_id.ids:
                            if rec.total_days > line.quantity:
                                invoice_line_values = {
                                    'name': rec.property_id.name,
                                    'price_unit': rec.rent_lease_amount,
                                    'price_subtotal': difference_amount,
                                    'quantity': difference_qty,
                                    'line_id': rec.id
                                }
                                lines.clear()
                                lines.append(Command.create(invoice_line_values))
                    if rec.id not in posted_invoice.invoice_line_ids.line_id.ids:
                        invoice_line_values = {
                            'name': rec.property_id.name,
                            'price_unit': rec.rent_lease_amount,
                            'price_subtotal': rec.total_amount,
                            'quantity': rec.total_days,
                            'line_id': rec.id
                        }
                        lines.append(Command.create(invoice_line_values))
                if lines:
                    invoice_vals = {
                        'partner_id': self.tenant_id.id,
                        'move_type': 'out_invoice',
                        'date': fields.Date.today(),
                        'invoice_date': fields.Date.today(),
                        'invoice_line_ids': lines,
                        'rental_lease_id': self.id
                    }
                    new_invoice = self.env['account.move'].create(invoice_vals)
                    return {
                        'type': 'ir.actions.act_window',
                        'res_model': 'account.move',
                        'view_type': 'tree,form',
                        'view_mode': 'form',
                        'res_id': new_invoice.id,
                        'view_id': (self.env.ref('account.view_move_form').id, 'form'),
                    }
        else:
            # new invoice
            lines = []
            for rec in self.property_ids:
                invoice_line_values = {
                    'name': rec.property_id.name,
                    'price_unit': rec.rent_lease_amount,
                    'price_subtotal': rec.total_amount,
                    'quantity': rec.total_days,
                    'line_id': rec.id
                    }
                lines.append(Command.create(invoice_line_values))
            invoice_vals = {
                'partner_id': self.tenant_id.id,
                'move_type': 'out_invoice',
                'date': fields.Date.today(),
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': lines,
                'rental_lease_id': self.id
            }
            new_invoice = self.env['account.move'].create(invoice_vals)

            self.message_post_with_source(
                'mail.message_origin_link',
                render_values={'self': self, 'origin': new_invoice},
                subtype_xmlid='mail.mt_note',
            )
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'view_type': 'tree,form',
                'view_mode': 'form',
                'res_id': new_invoice.id,
                'view_id': (self.env.ref('account.view_move_form').id, 'form'),
            }

    def _cron_expiry(self):
        today = fields.Date.today()
        expired = self.search([('due_date', '<', today), ('state', '!=', 'expired'),
                               ('state', '=', 'confirmed')])

        for rec in expired:
            if not rec.invoice_ids:
                rec.state = 'expired'
            template = self.env.ref('property_management.email_template_expired')
            template.send_mail(rec.id, force_send=True)

    def _cron_payment_due(self):
        today = fields.Date.today()
        payment_due = self.search([('due_date', '=', today), ('state', '=', 'confirmed'),
                                   ('payment_state', '!=', 'paid')])
        for rec in payment_due:
            if rec.invoice_ids:
                template = self.env.ref('property_management.email_template_payment_due')
                template.send_mail(rec.id, force_send=True)
