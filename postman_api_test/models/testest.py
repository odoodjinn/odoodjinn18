from odoo import fields, models


class TestTest(models.Model):
    _name = 'test.test'
    _inherits = {'todo': 'todo_field'}

    todo_field = fields.Many2one('todo')
