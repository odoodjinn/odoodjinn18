# -*- coding: utf-8 -*-

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    experience = fields.Integer(string='Experience', compute='_compute_experience')

    @api.model
    def get_tiles_data(self):
        """ Return the tile data"""
        user_id = self.env.user
        employee_attendance = self.env['hr.attendance'].sudo().search([])
        employee_leave = self.env['hr.leave'].sudo().search([])
        employee_project = self.env['project.project'].sudo().search([])
        attendance = employee_attendance.filtered(lambda x: x.employee_id.user_id == user_id)
        leave = employee_leave.filtered(lambda x: x.employee_id.user_id == user_id)
        project = employee_project.filtered(lambda x: x.user_id == user_id)
        return {
            'total_attendance': len(attendance),
            'total_leave': len(leave),
            'total_project': len(project),
        }

    def _compute_experience(self):
        """compute the experience of the employee using the create_date of the record on model"""
        today = fields.Datetime.today()
        for rec in self:
            rec.experience = (today-rec.create_date).days/365
