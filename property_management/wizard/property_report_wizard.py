# -*- coding: utf-8 -*-

import io
import json
import xlsxwriter
from odoo import fields, models
from odoo.tools import date_utils
from odoo.exceptions import ValidationError


class PropertyReportWizard(models.TransientModel):
    _name = 'property.report.wizard'
    _description = 'Property Report Wizard'

    name = fields.Many2one('rental.lease.management', string='Rental/Lease')
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    state = fields.Selection([('to_approve', 'To Approve'), ('draft', 'Draft'), ('confirmed', 'Confirmed'),
                              ('closed', 'Closed'), ('returned', 'Returned'), ('expired', 'Expired')],
                             string='State', readonly=False)
    tenant_id = fields.Many2one('res.partner', string='Tenant')
    owner_id = fields.Many2one('res.partner', string='Owner')
    type = fields.Selection([('rent', 'Rent'), ('lease', 'Lease')], string='Type')
    property_id = fields.Many2one('property.details', string='Property')

    def action_print_rental_report(self):
        """Print button to download the PDF file by fetching the data from database of the Rental/Lease model."""
        self.get_wizard_filters()
        records = self.env.cr.dictfetchall()
        state_dict = dict(self.env['rental.lease.management']._fields['state'].selection)
        type_dict = dict(self.env['rental.lease.management']._fields['type'].selection)
        if not records:
            raise ValidationError('There are no records found for the filter you have entered!')
        return self.env.ref('property_management.action_report_rental_lease_management').report_action(
            self, data={'records': records, 'state_dict': state_dict, 'type_dict': type_dict})

    def action_print_excel_rental_report(self):
        """Print Excel button - Action to fetch data from the database as per the filters on
        reporting menu."""
        self.get_wizard_filters()
        records = self.env.cr.dictfetchall()
        if not records:
            raise ValidationError('There are no records found for the filter you have entered!')
        state_dict = dict(self.env['rental.lease.management']._fields['state'].selection)
        type_dict = dict(self.env['rental.lease.management']._fields['type'].selection)
        data = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'records': records,
            'state_dict': state_dict,
            'type_dict': type_dict
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'property.report.wizard',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Rental/Lease Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """Function to align and print the xlsx report using the datas fetched from the database."""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'left'})
        nums = workbook.add_format({'font_size': '10px', 'align': 'right'})
        sheet.merge_range('B2:N3', 'RENTAL/LEASE EXCEL REPORT', head)
        sheet.merge_range('B5:C5', 'Property', cell_format)
        sheet.merge_range('D5:E5', 'Tenant',cell_format)
        sheet.merge_range('F5:G5', 'Owner', cell_format)
        sheet.write('H5', 'Type', cell_format)
        sheet.write('I5', 'Amount', cell_format)
        sheet.merge_range('J5:K5', 'Start Date', cell_format)
        sheet.merge_range('L5:M5', 'End Date', cell_format)
        sheet.merge_range('N5:O5', 'State', cell_format)
        type_dict = data['type_dict']
        state_dict = data['state_dict']
        row = 5
        for rec in data['records']:
            row += 1
            sheet.merge_range(f'B{row}:C{row}', rec['name'], txt)
            sheet.merge_range(f'D{row}:E{row}', rec['tenant'], txt)
            sheet.merge_range(f'F{row}:G{row}', rec['owner'], txt)
            sheet.write(f'H{row}', type_dict.get(rec['type'], ''), txt)
            sheet.write(f'I{row}', rec['rent_lease_amount'], nums)
            sheet.merge_range(f'J{row}:K{row}', rec['start_date'], nums)
            sheet.merge_range(f'L{row}:M{row}', rec['end_date'], nums)
            sheet.merge_range(f'N{row}:O{row}', state_dict.get(rec['state'],''), txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

    def get_wizard_filters(self):
        params = []
        where_clause = " WHERE"
        if self.from_date and self.to_date:
            where_clause += " rlm.due_date BETWEEN %s AND %s"
            params = [self.from_date, self.to_date]
        elif self.from_date:
            where_clause += " rlm.due_date>=%s"
            params = [self.from_date]
        elif self.to_date:
            where_clause += " rlm.due_date<=%s"
            params = [self.to_date]
        else:
            where_clause += " true"
        if self.tenant_id:
            where_clause += " AND rlm.tenant_id=%s"
            params.append(self.tenant_id.id)
        if self.state:
            where_clause += " AND rlm.state=%s"
            params.append(self.state)
        if self.type:
            where_clause += " AND rlm.type=%s"
            params.append(self.type)
        if self.owner_id:
            where_clause += " AND rol.owner_id=%s"
            params.append(self.owner_id.id)
        if self.property_id:
            where_clause += " AND rol.property_id=%s"
            params.append(self.property_id.id)
        query = f""" SELECT rp_tenant.name AS tenant,rlm.state,rlm.type,rp_owner.name as owner,
                rol.start_date,rol.end_date,pd.name,rol.rent_lease_amount FROM rental_lease_management rlm 
                INNER JOIN rental_order_line rol ON rlm.id=rol.rental_id 
                LEFT JOIN property_details pd ON rol.property_id=pd.id
                LEFT JOIN res_partner rp_tenant ON rlm.tenant_id=rp_tenant.id
                LEFT JOIN res_partner rp_owner ON rol.owner_id=rp_owner.id
                %s """ % where_clause
        self.env.cr.execute(query, params)


