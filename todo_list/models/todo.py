# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools import date_utils


class ToDo(models.Model):
    _name = 'todo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'To Do'

    name = fields.Char(string='Summary', required=True)
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')],
                                string='Priority')
    due_date = fields.Date(string='Due Date', required=True, default=fields.Date.today())
    description = fields.Html(string='Description')
    state = fields.Selection([('1_today', 'Today'), ('2_plan', 'Planned'), ('3_expire', 'Expired'),
                              ('4_done', 'Done'), ('5_cancel', 'Cancelled')], default='1_today')
    user_id = fields.Many2one('res.users', string='Users', default=lambda self: self.env.user)
    recurring = fields.Boolean(string='Recurring')
    recurring_interval = fields.Integer(string='Repeat Every', default=1)
    recurring_unit = fields.Selection([('day', 'Days'), ('week', 'Weeks'), ('month', 'Months'),
                                       ('year', 'Years')], default='day')
    recurring_type = fields.Selection([('forever', 'Forever'), ('until', 'Until')], default='forever')
    recurring_until = fields.Date(string='Recurring End Date')

    @api.onchange('due_date')
    def _onchange_due_date(self):
        today = fields.Date.today()
        todo_obj = self.search([('state', 'not in', ['4_done','5_cancel'])])
        for record in todo_obj:
            if record.due_date:
                if record.due_date == today:
                    record.state = '1_today'
                elif record.due_date < today:
                    record.state = '3_expire'
                elif record.due_date > today:
                    record.state = '2_plan'

    def action_done(self):
        self.state = '4_done'

    def action_cancel(self):
        self.state = '5_cancel'

    def recurring_todo_activities(self):
        today = fields.Date.today()
        todo_obj = self.search([('state', '=', '4_done'),('recurring', '=', True)])
        for rec in todo_obj:
            recurring_date = ""
            if rec.recurring_unit == 'day':
                recurring_date = (date_utils.add(rec.create_date, days=rec.recurring_interval)).date()
            elif rec.recurring_unit == 'week':
                recurring_date = (date_utils.add(rec.create_date, weeks=rec.recurring_interval)).date()
            elif rec.recurring_unit == 'month':
                recurring_date = (date_utils.add(rec.create_date, months=rec.recurring_interval)).date()
            elif rec.recurring_unit == 'year':
                recurring_date = (date_utils.add(rec.create_date, years=rec.recurring_interval)).date()

            if rec.recurring_type == 'forever':
                if recurring_date == today:
                    rec.copy({
                        'name': rec.name + '(copy)',
                        'due_date': today,
                        'state': '1_today'
                    })
            else:
                if recurring_date <= today:
                    rec.copy({
                        'name': rec.name + '(copy)',
                        'due_date': today,
                        'state': '1_today'
                    })
