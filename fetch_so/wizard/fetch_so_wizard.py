# -*- coding: utf-8 -*-

import xmlrpc.client
import re

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
            so = self.env['sale.order'].search([('name', '=', rec['name'])]).id
            if not so:
                db_2_so = models_2.execute_kw(db_2, uid_db2, password_db_2, 'sale.order', 'create', [{
                    'id': rec['id'],
                    'name': rec['name'],
                    'partner_id': partner[0]['id'],
                    # 'state': rec['state'],
                    'amount_total': rec['amount_total']
                }])
                lines = rec['order_line']
                db_1_so_line = models_1.execute_kw(db_1, uid_db1, password_db_1, 'sale.order.line', 'search_read', [], {
                    'domain': [('id', 'in', lines)],
                    'fields': ['id', 'order_id', 'product_id', 'name', 'product_uom_qty', 'price_unit', 'price_subtotal'],
                })
                print(db_1_so_line,'/a')
                for line in db_1_so_line:
                    product_name = re.sub(r"\[.*?\]", "", line['product_id'][1])
                    product_name_new = product_name.strip()
                    sale_order = self.env['sale.order'].browse(db_2_so)
                    print(sale_order,'//so')
                    product_obj = self.env['product.template'].search([('name', '=', product_name_new)])
                    db_2_so_line = models_2.execute_kw(db_2, uid_db2, password_db_2, 'sale.order.line', 'create', [{
                        'name': product_name_new ,
                        'product_id': product_obj.id,
                        'product_uom_qty': line['product_uom_qty'],
                        'order_id': sale_order.id,
                        'price_unit': line['price_unit'],
                    }])


# PO in current Db
# first_message = f"Nothing to import from odoo{version}"
# count = 0
# for i in db_1_leads:
#     partner = self.env['res.partner'].search([('name', '=', i['partner_id'][1])])
#     purchase_order = self.env['purchase.order'].sudo().search([('name','=',i['name'])]).id
#     if not purchase_order:
#         purchase_order = models_2.execute_kw(db_2, uid_db2, password_db_2, 'purchase.order', 'create', [{
#             # 'id': i['id'],
#             'name': i['name'],
#             'partner_id': partner.id,
#             'amount_total': i['amount_total'],
#             # 'order_line': order_line[0],
#             'state': i['state'],
#             'date_approve': i['date_approve'],
#             'date_planned': i['date_planned'],
#             'currency_id': i['currency_id'][0]
#         }] )
#         order_line = models_1.execute_kw(db_1, uid_db1, password_db_1, 'purchase.order.line', 'search_read', [], {
#             'domain': [('order_id', '=', i['id'])]
#         })
#         for j in order_line:
#             prod_name= re.sub(r"\[.*?\]", "", j['product_id'][1])
#             product_name = prod_name.strip()
#             product_new = self.env['product.template'].search([('name','=',product_name)])
#             orders = self.env['purchase.order'].browse(purchase_order)
#             vals = {
#                 'name': j['name'],
#                 'product_id': product_new.id,
#                 'order_id': int(orders.id),
#                 'product_qty': j['product_qty'],
#                 'price_unit': j['price_unit'],
#                 'product_uom': j['product_uom'][0],
#                 'display_type':j['display_type']
#             }
#             models_2.execute_kw(db_2, uid_db2, password_db_2, 'purchase.order.line', 'create',[vals])
