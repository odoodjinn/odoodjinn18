# -*- coding: utf-8 -*-

{
    'name': 'To Do List',
    'version': '18.0.1.0.0',
    'category': 'To-Do',
    'summary': 'User can create General Todo activities',
    'description': """
        To schedule and listing out activities which should be done. User can create general ToDo activities, 
        prioritize each activity, assign recurrence on activities, filtering activities based on the user.
    """,
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/todo_views.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}
