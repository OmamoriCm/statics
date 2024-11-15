# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from datetime import datetime, timedelta
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
from openerp import workflow

class sale_order(osv.osv):
    
    def _amount_all_wrapper(self, cr, uid, ids, field_name, arg, context=None):
        """ Wrapper because of direct method passing as parameter for function fields """
        return self._amount_all(cr, uid, ids, field_name, arg, context=context)

    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        return super(sale_order, self)._amount_all(cr, uid, ids, field_name, arg, context=context)
    
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()
    
    _inherit = 'sale.order'
    _columns = {
        'amount_untaxed': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Untaxed Amount',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty','edited'], 10),
            },
            multi='sums', help="The amount without tax.", track_visibility='always'),
        'amount_tax': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Taxes',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty','edited'], 10),
            },
            multi='sums', help="The tax amount."),
        'amount_total': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Total',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty','edited'], 10),
            },
            multi='sums', help="The total amount."),
    }
    def button_dummy(self, cr, uid, ids, context=None):
        #=============================add dummy line============================
        if not ids:
            return True
        obj_sale_order_line = self.pool.get('sale.order.line')
        for order in self.browse(cr, uid, ids, context=None):
            if order.order_line:
                for line in order.order_line:
                    line.refresh()
                    obj_sale_order_line.button_dummy_line(cr, uid, [line.id], context=None)
        #=======================================================================
        return True
    

class sale_order_line(osv.osv):
    
    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        res = {}
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            #=========================discount multi============================
            if line.product_id and line.product_id.customer_discount_ids:
                for cust_disc in line.product_id.customer_discount_ids:
                    if line.order_id.partner_id and line.order_id.partner_id.partner_group_id == cust_disc.name:
                        #print "partner_ini",line.order_id.partner_id.partner_group_id,cust_disc.name
                        for multi_disc in cust_disc.discount_ids:
                            price = price * (1 - (multi_disc.name or 0.0) / 100.0)
            #===================================================================
            taxes = tax_obj.compute_all(cr, uid, line.tax_id, price, line.product_uom_qty, line.product_id, line.order_id.partner_id)
            cur = line.order_id.pricelist_id.currency_id
            res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
        return res
        
    def _show_discount_line_multi(self, cr, uid, ids, name, args, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = ''
            wheres = []
            if line.product_id and line.product_id.customer_discount_ids:
                for cust_disc in line.product_id.customer_discount_ids:
                    if line.order_id.partner_id and line.order_id.partner_id.partner_group_id == cust_disc.name:
                        for multi_disc in cust_disc.discount_ids:
                            wheres.append(str(multi_disc.name)+'%')
            if len(wheres) == 1:
                res[line.id] = "".join(wheres)
            else:
                res[line.id] = ", ".join(wheres)
        return res
    
    _inherit = "sale.order.line"
    _description = "Sales Order Line"
    _columns = {
        'edited': fields.integer('Edited'),
        'show_discount_line': fields.function(_show_discount_line_multi, string='Discount Multiple', type='char', readonly=True),
        'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')),
    }
    _default = {
        'edited': 0,
    }
    def button_dummy_line(self, cr, uid, ids, context=None):
        if not ids:
            return True
        for line in self.browse(cr, uid, ids, context=None):
            count = line.edited+1
            self.write(cr, uid, [line.id], {'edited': count})
        return True