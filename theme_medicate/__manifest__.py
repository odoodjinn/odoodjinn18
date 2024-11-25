# -*- coding: utf-8 -*-
{
    'name': 'Theme Medicate',
    'version': '18.0.1.0.0',
    'category': 'Theme/eCommerce',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'depends': ['base','website'],
    'data': [
        'views/header_templates.xml',
        'views/footer_templates.xml',
        'views/snippets/home_page_carousel_template.xml',
        'views/snippets/home_page_about_template.xml',
        'views/snippets/home_page_facility_provided_template.xml',
        'views/snippets/home_page_about_content_template.xml',
        'views/snippets/home_page_great_work_template.xml',
        'views/snippets/home_page_working_progress_template.xml',
        'views/snippets/home_page_heart_specialists_template.xml',
        'views/snippets/home_page_clients_template.xml',
        'views/snippets.xml',
        'views/homepage_snippets.xml',
    ],
'assets': {
        'web.assets_frontend': [
            'theme_medicate/static/src/css/main.css',
        ],
        'web.assets_backend': [
            "theme_medicate/static/src/js/welcome_message.js"
        ],
},
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
