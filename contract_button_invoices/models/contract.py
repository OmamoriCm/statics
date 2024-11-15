# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.addons.decimal_precision import decimal_precision as dp


class AccountAnalyticInvoiceLine(models.Model):
    _inherit = "account.analytic.invoice.line"

    @api.one
    @api.depends('price_unit', 'discount')
    def _amount_line(self):
        currency_obj = self.env['res.currency']
        discount = self.discount / 100
        price_subtotal = self.quantity * self.price_unit * (1 - discount)
        if self.analytic_account_id.pricelist_id:
            cur = self.analytic_account_id.pricelist_id.currency_id
            price_subtotal = cur.round(price_subtotal)
        self.price_subtotal = price_subtotal

    discount = fields.Float(
        string='Discount (%)',
        digits=dp.get_precision('Discount'),
        default=0.0,
        required=True,
        help="e.g. 21, 16...")

    price_subtotal = fields.Float(
        string='Sub Total',
        digits=dp.get_precision('Account'),
        compute='_amount_line')

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    
    def _prepare_invoice_data(self, cr, uid, contract, context=None):
        print("entro en prepare invoice data")
        context = context or {}
        invoice = super(AccountAnalyticAccount,self)._prepare_invoice_data(cr, uid, contract, context=context)
        invoice.update({
            'analytic_account_id': contract.id,
            })
        return invoice
    