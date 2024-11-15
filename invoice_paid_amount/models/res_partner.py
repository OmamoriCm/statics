# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from openerp import api, models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    invoice_paid_amount = fields.Float(compute='_get_invoice_paid_amount', string='Invoice Paid Amount', help='This field will give the invoice paaid amount of the particular customer.')

    #For getting the invoice paid amount of the customer
    @api.one
    def _get_invoice_paid_amount(self):
        for record in self:
            paid_amount = open_amount = total_amount = 0.0
            invoice_paid_ids = self.env['account.invoice'].sudo().search([('partner_id', '=', record.id),('state', '=', 'paid'),('type','in', ('out_invoice', 'out_refund'))])
            if invoice_paid_ids:
                for invoice in invoice_paid_ids:
                    paid_amount += invoice.amount_total
            invoice_open_ids = self.env['account.invoice'].sudo().search([('partner_id', '=', record.id),('state', 'not in', ['draft', 'cancel','paid']),('type','in', ('out_invoice', 'out_refund'))])
            if invoice_open_ids:
                for invoice in invoice_open_ids:
                    if invoice.residual > 0:
                        open_amount += (invoice.amount_total - invoice.residual)
            total_amount = open_amount + paid_amount
            record.invoice_paid_amount = total_amount

