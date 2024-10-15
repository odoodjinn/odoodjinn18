# -*- coding: utf-8 -*-
{
    'name': 'Employee Dashboard V17',
    'version': '18.0.1.0.0',
    'category': 'Dashboard',
    'summary': 'Employee dashboard with all details',
    'description': """
        This module displays all the details about employee in the dashboard app.
    """,
    'depends': ['base', 'hr'],
    'data': [
        'views/employee_dashboard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'employee_dashboard/static/src/js/dashboard.js',
            'employee_dashboard/static/src/xml/dashboard.xml',
        ],
    },

    'license': 'LGPL-3',
}
