# -*- coding: utf-8 -*-

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    experience = fields.Integer(string='Experience', compute='_compute_experience')

    @api.model
    def get_tiles_data(self):
        """ Return the tile data"""
        user_id = self.env.user
        employee_data = self.sudo().search([])
        employee_attendance = self.env['hr.attendance'].sudo().search([])
        employee_leave = self.env['hr.leave'].sudo().search([])
        employee_project = self.env['project.project'].sudo().search([])
        employee_self = employee_data.filtered(lambda x: x.user_id == user_id)
        attendance = employee_attendance.filtered(lambda x: x.employee_id.user_id == user_id)
        leave = employee_leave.filtered(lambda x: x.employee_id.user_id == user_id)
        project = employee_project.filtered(lambda x: x.user_id == user_id)
        today = fields.Datetime.today()
        experience = (today-employee_self.create_date).days/365
        print(employee_self.create_date,'//selfprint')
        employee_info = {
            'id': employee_self.id,
            'name': employee_self.name,
            'position': employee_self.job_id.name,
            'department': employee_self.department_id.name,
            'experience': int(experience),

        }
        return {
            'user_id': user_id,
            'total_employee': len(employee_data),
            'total_attendance': len(attendance),
            'total_leave': len(leave),
            'total_project': len(project),
            'employee_info': employee_info,
        }

    def _compute_experience(self):
        for rec in self:
            rec.experience = (fields.Datetime.today()-rec.create_date).days/365
