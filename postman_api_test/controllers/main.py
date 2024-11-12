# -*- coding: utf-8 -*-
import json

from odoo import http
from odoo.http import request, Controller, Response


class PostmanApiController(Controller):
    @http.route('/api/create_rec/partner', type='http', auth='none', csrf=False)
    def create_rec(self):
        """Function to create a record in 'res.partner' through Postman API"""
        data = request.get_json_data()
        if not data.get('name'):
            return Response(
                json.dumps({
                'status': 'error',
                'message': 'Name is required'
                }), content_type='application/json')
        partner = request.env['res.partner'].sudo().create({
            'name': data.get('name'),
            'email': data.get('email', False),
        })
        response_data = {
            'success': True,
            'message': 'Partner created successfully',
            'data': {
                'id': partner.id,
                'name': partner.name,
                'email': partner.email,
            }
        }
        return Response(
            json.dumps(response_data),
            content_type='application/json',
        )
