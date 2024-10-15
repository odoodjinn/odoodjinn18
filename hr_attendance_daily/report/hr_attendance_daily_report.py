# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrAttendanceDailyReport(models.AbstractModel):
    _name = 'report.hr_attendance_daily.report_hr_attendance_daily'
    _description = 'Daily Attendance Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """ Fetch data from the wizard model and attendance model,
        and then return to the qweb template to print the pdf."""
        if data['print_by'] == 'daily':
            attendance_obj = self.env['hr.attendance'].search([
                ('check_in', '>=', data['today']),
                ('check_out', '<=', data['today']),
            ])
            if not attendance_obj:
                raise ValidationError('No such records found!')

        elif data['print_by'] == 'weekly':
            attendance_obj = self.env['hr.attendance'].search([
                ('check_in', '>=', data['starting_week']),
                ('check_out', '<=', data['ending_week']),
            ])
            if not attendance_obj:
                raise ValidationError('No such records found!')
        elif data['print_by'] == 'monthly':
            attendance_obj = self.env['hr.attendance'].search([
                ('check_in', '>=', data['starting_month']),
                ('check_out', '<=', data['ending_month']),
            ])
            if not attendance_obj:
                raise ValidationError('No such records found!')
        else:
            attendance_obj = self.env['hr.attendance'].search([
                ('check_in', '>=', data['start_date']),
                ('check_out', '<=', data['end_date']),
            ])
            if not attendance_obj:
                raise ValidationError('No such records found!')
        return {
            'docs': attendance_obj,
        }
