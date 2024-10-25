# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools import date_utils



class ToDo(models.Model):
    _name = 'todo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'To Do'

    name = fields.Char(string='Summary', required=True)
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    due_date = fields.Date(string='Due Date', required=True, default=fields.Date.today())
    recurring = fields.Boolean(string='Recurring')
    description = fields.Html(string='Description')
    state = fields.Selection([('1_today', 'Today'), ('2_plan', 'Planned'), ('3_expire', 'Expired'), ('4_done', 'Done'), ('5_cancel', 'Cancelled')])
    user_ids = fields.Many2many('res.users', string='Users')
    recurring_interval = fields.Integer(string='Repeat Every', default=1)
    recurring_type = fields.Selection([('day', 'Days'), ('week', 'Weeks'), ('month', 'Months'), ('year', 'Years')], default='week')
    recurring_end = fields.Selection([('forever', 'Forever'), ('until', 'Until')], default='forever')
    recurring_end_date = fields.Date(string='Recurring End Date')

    def action_done(self):
        self.state = '4_done'

    def action_cancel(self):
        self.state = '5_cancel'

    @api.onchange('due_date')
    def _onchange_state(self):
        today = fields.Date.today()
        for rec in self:
            if rec.due_date:
                if rec.due_date == today:
                    rec.state = '1_today'
                elif rec.due_date < today:
                    rec.state = '3_expire'
                elif rec.due_date > today:
                    rec.state = '2_plan'
