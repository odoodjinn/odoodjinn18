# -*- coding: utf-8 -*-

from odoo.addons.portal.controllers.portal import CustomerPortal

from odoo import http
from odoo.http import request


class CustomerPortalQuote(CustomerPortal):
    @http.route(['/my/orders/<int:order_id>/confirm'], type='http', auth="public", methods=['POST'], website=True)
    def portal_quote_confirm(self, order_id, access_token=None):
        """function to confirm the Quotation by calling the default 'action_confirm' function"""
        order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        order_sudo.action_confirm()
        redirect_url = order_sudo.get_portal_url(query_string="&message=sign_ok")
        return request.redirect(redirect_url)
