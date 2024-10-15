# -*- coding: utf-8 -*-

{
    'name': 'Spotter Sale Order Approval',
    'version': '18.0.1.0.0',
    'category': 'Sale',
    'summary': 'Sale Order Approval (Above 25k)',
    'description': """
        This module prevents approval of sale orders if the amount is greater than 25K.
    """,
    'depends': ['base', 'sale'],
    'data': [
        'views/sale_order_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
