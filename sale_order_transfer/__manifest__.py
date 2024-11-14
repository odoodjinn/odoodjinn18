# -*- coding: utf-8 -*-
{
    'name': 'Sale Order Transfer',
    'version': '18.0.1.0.0',
    'category': 'Sales/Ecommerce',
    'summary': 'User can transfer SO between companies',
    'depends': ['base', 'sale', 'web', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'wizard/sale_order_transfer_wizard.xml',
    ],
    'license': 'LGPL-3',
}
