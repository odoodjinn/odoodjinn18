# -*- coding: utf-8 -*-

import xmlrpc.client
from itertools import product

from odoo import models


class FetchSoWizard(models.TransientModel):
    _name = 'fetch.so.wizard'
    _description = 'Fetch Sale Orders Wizard'

    def action_fetch_records(self):
        """Button action to fetch sale order records from odoo17 db to current odoo18 db"""
        url_db1 = "http://localhost:8016"
        db_1 = 'odoo17_migration'
        username_db_1 = 'admin'
        password_db_1 = 'cool'
        common_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db1))
        models_1 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db1))
        version_db1 = common_1.version()

        url_db2 = "http://localhost:8018"
        db_2 = 'odoo18_migration'
        username_db_2 = 'admin'
        password_db_2 = 'cool'
        common_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db2))
        models_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db2))
        version_db2 = common_2.version()

        uid_db1 = common_1.authenticate(db_1, username_db_1, password_db_1, {})
        uid_db2 = common_2.authenticate(db_2, username_db_2, password_db_2, {})

        db_1_so = models_1.execute_kw(db_1, uid_db1, password_db_1, 'sale.order', 'search_read', [], {
            'fields': ['name', 'partner_id', 'user_id', 'amount_total', 'order_line', 'state'],
            'domain': [('state', '=', 'sale')]
        })
        db_1_partner = models_1.execute_kw(db_1, uid_db1, password_db_1, 'res.partner', 'search_read', [],
                                           {'fields': ['id', 'name', 'email']})
        db_1_product = models_1.execute_kw(db_1, uid_db1, password_db_1, 'product.template', 'search_read', [],
                                           {'fields': ['id', 'name', 'list_price']})
        for rec in db_1_partner:
            partner_rec = self.env['res.partner'].search_read([('name', '=', rec['name'])], [])
            if not partner_rec:
                db_2_partner = models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'create', [rec])

        for rec in db_1_product:
            product_rec = self.env['product.template'].search_read([('name', '=', rec['name'])], [])
            if not product_rec:
                db_2_product = models_2.execute_kw(db_2, uid_db2, password_db_2, 'product.template', 'create', [rec])

        for rec in db_1_so:
            partner = self.env['res.partner'].search_read([('name', '=', rec['partner_id'][1])])
            so = self.env['sale.order'].search_read([('name', '=', rec['name'])], [])
            if not so:
                db_2_so = models_2.execute_kw(db_2, uid_db2, password_db_2, 'sale.order', 'create', [{
                    'name': rec['name'],
                    'partner_id': partner[0]['id'],
                    # 'state': rec['state'],
                    'amount_total': rec['amount_total']
                    }])
                # print(self.env['sale.order'].browse(db_2_so))
            lines = rec['order_line']
            for line in lines:
                db_1_so_line = models_1.execute_kw(db_1, uid_db1, password_db_1, 'sale.order.line', 'search_read', [], {
                    'domain': [('id', '=', line)],
                    'fields': ['id', 'order_id', 'product_id', 'name', 'product_uom_qty', 'price_unit', 'price_subtotal'],
                })
                print(db_1_so_line)
                # for product in db_1_so_line:
                # print(product,'//product')
                # db_2_so_line = models_2.execute_kw(db_2, uid_db2, password_db_2, 'sale.order.line', 'create', [{
                #     'product_id': db_1_so_line[0]['product_id'][0],
                # }])

                # print(db_2_so_line,'//db2')
                order_ref = db_1_so_line[0]['order_id'][1]
                print(order_ref,'//inverse to so')
