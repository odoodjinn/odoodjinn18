# -*- coding: utf-8 -*-

from odoo import fields, models


class ToDo(models.Model):
    _name = 'todo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'To Do'

    name = fields.Char(string='Summary')
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    due_date = fields.Date(string='Due Date', default=fields.Date.today())
    recurring = fields.Boolean(string='Recurring')
    description = fields.Html(string='Description')
    state = fields.Selection([('today', 'Today'), ('plan', 'Planned'), ('expire', 'Expired'), ('done', 'Done'), ('cancel', 'Cancelled')])

    def action_done(self):
        self.state = 'done'
        
    def action_cancel(self):
        self.state = 'cancel'