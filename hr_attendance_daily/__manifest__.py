# -*- coding: utf-8 -*-

{
    'name': 'Daily Wise Attendance',
    'version': '18.0.1.0.0',
    'category': 'Attendance',
    'summary': 'Daily wise attendance report',
    'description': """
        This module prints daily wise attendance report.
    """,
    'depends': ['base', 'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/hr_attendance_daily_wizard.xml',
        'report/ir_actions_report.xml',
        'report/hr_attendance_daily_report_template.xml',
    ],
    'license': 'LGPL-3',
}
