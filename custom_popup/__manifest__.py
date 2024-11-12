# -*- coding: utf-8 -*-

{
    'name': 'Custom Popup',
    'version': '18.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Custom popup on numpad click',
    'depends': ['base', 'point_of_sale'],
    'assets': {
       'point_of_sale._assets_pos': [
           'custom_popup/static/src/js/templates.js',
           'custom_popup/static/src/xml/templates.xml',
       ],
    },
    'license': 'LGPL-3',
}
