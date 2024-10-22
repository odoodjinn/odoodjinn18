# -*- coding: utf-8 -*-

import xmlrpc.client
import re

from odoo import fields, models
from odoo.exceptions import ValidationError


class FetchSoWizard(models.TransientModel):
    _name = 'fetch.so.wizard'
    _description = 'Fetch Sale Orders Wizard'

    type = fields.Selection([('api', 'API Key'), ('uid', 'User Credentials')], default='api')
    api_code = fields.Char(string='Api Code')
    username_db_1 = fields.Char(string='User Name')
    password_db_1 = fields.Char(string='Password')
    url_db1 = fields.Char(string='URL', default='http://localhost:8016')
    db_1 = fields.Char(string='Database Name', default='odoo17_migration')

    def action_fetch_records(self):
        """Button action to fetch sale order records from odoo17 db to current odoo18 db"""
        url_db1 = self.url_db1
        db_1 = self.db_1
        username_db_1 = self.username_db_1
        if self.type == 'uid':
            password_db_1 = self.password_db_1
        else:
            password_db_1 = self.api_code

        common_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db1))
        models_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db1))
        version_db1 = common_1.version()

        current_db = self.env.cr.dbname

        url_db2 = "http://localhost:8018"
        db_2 = current_db
        username_db_2 = 'admin'
        password_db_2 = 'cool'
        common_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db2))
        models_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db2))
        version_db2 = common_2.version()
        print(db_1,username_db_1,password_db_1,'/test')
        try:
            uid_db1 = common_1.authenticate(db_1, username_db_1, password_db_1, {})
        except:
            raise ValidationError('Check your first database credentials')
        try:
            uid_db2 = common_2.authenticate(db_2, username_db_2, password_db_2, {})
        except:
            raise ValidationError('Check your second database credentials')
        db_1_so = models_1.execute_kw(db_1, uid_db1, password_db_1, 'sale.order', 'search_read', [], {
            'fields': ['name', 'partner_id', 'user_id', 'amount_total', 'order_line', 'state']
        })
        db_1_partner = models_1.execute_kw(db_1, uid_db1, password_db_1, 'res.partner', 'search_read', [],
                                           {'fields': ['id', 'name', 'email']})
        db_1_product = models_1.execute_kw(db_1, uid_db1, password_db_1, 'product.template', 'search_read', [],
                                           {'fields': ['id', 'name', 'list_price']})
        for partner in db_1_partner:
            partner_rec = self.env['res.partner'].search_read([('name', '=', partner['name'])], [])
            if not partner_rec:
                db_2_partner = models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'create', [partner])
        for product in db_1_product:
            product_rec = self.env['product.template'].search_read([('name', '=', product['name'])], [])
            if not product_rec:
                db_2_product = models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.template', 'create', [product])

        for rec in db_1_so:
            so = self.env['sale.order'].search([('name', '=', rec['name'])]).id
            partner_name = rec['partner_id'][1]
            partner = models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'search_read', [
                [('name', '=', partner_name)], []
            ])
            if not so:
                if partner:
                    db_2_so = models_2.execute_kw(db_2, uid_db2, password_db_2, 'sale.order', 'create', [{
                        'id': rec['id'],
                        'name': rec['name'],
                        'partner_id': partner[0]['id'],
                        'state': rec['state'],
                        'amount_total': rec['amount_total']
                    }])
                    lines = rec['order_line']
                    db_1_so_line = models_1.execute_kw(db_1, uid_db1, password_db_1, 'sale.order.line', 'search_read', [], {
                        'domain': [('id', 'in', lines)],
                        'fields': ['id', 'order_id', 'product_id', 'name', 'product_uom_qty', 'price_unit', 'price_subtotal'],
                    })
                    for line in db_1_so_line:
                        product_name = re.sub(r"\[.*?\]", "", line['product_id'][1])
                        product_name_new = product_name.strip()
                        sale_order = self.env['sale.order'].browse(db_2_so)
                        product_obj = self.env['product.template'].search([('name', '=', product_name_new)])
                        db_2_so_line = models_2.execute_kw(db_2, uid_db2, password_db_2, 'sale.order.line', 'create', [{
                            'name': product_name_new ,
                            'product_id': product_obj.id,
                            'product_uom_qty': line['product_uom_qty'],
                            'order_id': sale_order.id,
                            'price_unit': line['price_unit'],
                        }])
