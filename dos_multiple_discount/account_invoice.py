##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 
#    2004-2010 Tiny SPRL (<http://tiny.be>). 
#    2009-2010 Veritos (http://veritos.nl).
#    All Rights Reserved
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
##############################################################################

import itertools
from lxml import etree

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp.tools import float_compare
import openerp.addons.decimal_precision as dp

class account_invoice_line(models.Model):
    _inherit = "account.invoice.line"
    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_id', 'quantity', 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id')
    def _compute_price(self):
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        #=========================discount multi============================
        if self.product_id and self.product_id.customer_discount_ids:
            for cust_disc in self.product_id.customer_discount_ids:
                if self.invoice_id.partner_id and self.invoice_id.partner_id.partner_group_id == cust_disc.name:
                    for multi_disc in cust_disc.discount_ids:
                        price = price * (1 - (multi_disc.name or 0.0) / 100.0)
        #===================================================================
        taxes = self.invoice_line_tax_id.compute_all(price, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
        self.price_subtotal = taxes['total']
        if self.invoice_id:
            self.price_subtotal = self.invoice_id.currency_id.round(self.price_subtotal)
            
    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_id', 'quantity', 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id')            
    def _show_discount_line_multi(self):
        wheres = []
        multiple_disc = ''
        if self.product_id and self.product_id.customer_discount_ids:
            for cust_disc in self.product_id.customer_discount_ids:
                if self.invoice_id.partner_id and self.invoice_id.partner_id.partner_group_id == cust_disc.name:
                    for multi_disc in cust_disc.discount_ids:
                        wheres.append(str(multi_disc.name)+'%')
            if len(wheres) == 1:
                multiple_disc = "".join(wheres)
            else:
                multiple_disc = ", ".join(wheres)
        #print "multiple_disc",multiple_disc
        if multiple_disc:
            self.show_discount_line = multiple_disc
            
    price_subtotal = fields.Float(string='Amount', digits= dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_price')
    show_discount_line = fields.Char(string='Discount Multiple',  
        store=False, readonly=True, compute='_show_discount_line_multi')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
