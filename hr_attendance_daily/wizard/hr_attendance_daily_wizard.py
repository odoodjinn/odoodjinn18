# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.tools import date_utils


class HrAttendanceDailyWizard(models.TransientModel):
    _name = 'hr.attendance.daily.wizard'
    _description = 'Daily Attendance Report Wizard'

    print_by = fields.Selection([('daily', 'Daily'),('weekly', 'Weekly'), ('monthly', 'Monthly'), ('custom', 'Custom')],string='Print By', default='daily')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    def action_print_report(self):
        """Print button action on the wizard to pass the filter data to the abstract model
            and print the pdf"""
        today = fields.Date.today()
        starting_week = date_utils.start_of(today, "week")
        ending_week = date_utils.end_of(today, "week")
        starting_month = date_utils.start_of(today, "month")
        ending_month = date_utils.end_of(today, "month")

        data = {
            'today': today,
            'print_by': self.print_by,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'starting_week': starting_week,
            'ending_week': ending_week,
            'starting_month': starting_month,
            'ending_month': ending_month,
        }
        return self.env.ref('hr_attendance_daily.action_report_hr_attendance_daily').report_action(
            None, data=data)
