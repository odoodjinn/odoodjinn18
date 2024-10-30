# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools import date_utils

STAGES = ['Today', 'Planned', 'Expired', 'Done', 'Cancelled']


class ToDoStage(models.Model):
    _name = 'todo.stage'
    _description = 'To Do Stage'
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True, translate=True)
    sequence = fields.Integer(string='Sequence')
    stage_ids = fields.One2many('todo', 'stage_id')


class ToDo(models.Model):
    _name = 'todo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'To Do'

    @api.returns('self')
    def _default_stage(self):
        return self.env['todo.stage'].search([], limit=1)

    name = fields.Char(string='Summary', required=True)
    stage_id = fields.Many2one('todo.stage', string='Stages', default=_default_stage, group_expand='_read_group_stage_ids')
    state = fields.Selection([('today', 'Today'), ('plan', 'Planned'), ('expire', 'Expired'),
                              ('done', 'Done'), ('cancel', 'Cancelled')])
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')],
                                string='Priority', default='0')
    due_date = fields.Date(string='Due Date', required=True, default=fields.Date.today())
    description = fields.Html(string='Description')
    user_id = fields.Many2one('res.users', string='Users', default=lambda self: self.env.user)
    recurring = fields.Boolean(string='Recurring')
    recurring_interval = fields.Integer(string='Repeat Every', default=1)
    recurring_unit = fields.Selection([('day', 'Days'), ('week', 'Weeks'), ('month', 'Months'),
                                       ('year', 'Years')], default='day')
    recurring_type = fields.Selection([('forever', 'Forever'), ('until', 'Until')], default='forever')
    recurring_until = fields.Date(string='Recurring End Date')

    @api.onchange('due_date')
    def _onchange_due_date(self):
        """Function in scheduled action to change stages based on due date"""
        self._change_state()

    def action_done(self):
        """Mark As Done button in the form view to change the stage into Done"""
        stage_obj = self.env['todo.stage'].search([('name', '=', 'Done')])
        self.stage_id = stage_obj
        self.state = 'done'

    def action_cancel(self):
        """Cancel button in the form view to change the stage into Cancelled"""
        stage_obj = self.env['todo.stage'].search([('name', '=', 'Cancelled')])
        self.stage_id = stage_obj
        self.state = 'cancel'

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        """ Read group customization in order to display all the stages in the
            kanban view, even if they are empty
        """
        stage_ids = stages.sudo()._search([], order=stages._order)
        return stages.browse(stage_ids)

    def _change_state(self):
        """Function to change the stages based on due date"""
        today = fields.Date.today()
        todo_obj = self.search([('state', 'not in', ['done', 'cancel'])])
        stage_obj = self.env['todo.stage'].search([])
        for record in todo_obj:
            for rec in stage_obj:
                if record.due_date:
                    if record.due_date == today:
                        if rec.name == STAGES[0]:
                            record.stage_id = rec
                            record.state = 'today'
                    elif record.due_date > today:
                        if rec.name == STAGES[1]:
                            record.stage_id = rec
                            record.state = 'plan'
                    elif record.due_date < today:
                        if rec.name == STAGES[2]:
                            record.stage_id = rec
                            record.state = 'expire'

    def _recurring_todo_activities(self):
        """Scheduled action function to create recurring To-Do activities"""
        today = fields.Date.today()
        todo_obj = self.search([('recurring', '=', True),('state', '!=', 'cancel')])
        stage_obj = self.env['todo.stage'].search([('name', '=', 'Today')])
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
                        'stage_id': stage_obj.id,
                    })
            else:
                if recurring_date <= today:
                    rec.copy({
                        'name': rec.name + '(copy)',
                        'due_date': today,
                        'stage_id': stage_obj.id,
                    })
