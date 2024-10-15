# -*- coding: utf-8 -*-

{
    'name': 'Ordered Quantity Invoice',
    'version': '18.0.1.0.0',
    'category': 'Sale/Invoice',
    'summary': 'Selected partners can only create invoice with ordered quantities',
    'description': """
        This module provide a boolean field inside the contact app to select the partner 
        who can only get the SO with the invoicing policy for Ordered Qty.
    """,
    'depends': ['base', 'sale', 'contacts'],
    'data': [
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
    ],
    'license': 'LGPL-3',
}