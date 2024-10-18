# -*- coding: utf-8 -*-
{
    'name': 'Fetch Sale Orders V17',
    'version': '18.0.1.0.0',
    'category': 'Sale',
    'summary': 'Fetch records from odoo17 database',
    'description': """
        This module fetch all records from odoo17 database and displays in odoo18 database.
    """,
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/fetch_so_wizard_views.xml',
    ],
    'license': 'LGPL-3',
}
