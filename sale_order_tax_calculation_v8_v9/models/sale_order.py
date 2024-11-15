# -*- coding: utf-8 -*-
# (c) 2017 Vignesh
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models,fields,api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sub_with_tax=fields.Float(string="Subtotal tax")


class SaleOrder(models.Model):

    _inherit = 'sale.order'
    
#    show_tax = fields.Many2many('account.tax',string= "show taxes")
    
    @api.onchange('order_line','order_line.tax_id','order_line.price_subtotal','order_line.product_uom_qty','order_line.product_id')
    def onchange_tax(self):
        if self.order_line:
            for line in self:
                for order in line.order_line:
                    if order.tax_id:
                        total_tax = 0.0
                        for tax in order.tax_id:
                            total_tax += tax.amount
                        values = (order.price_subtotal/100)*total_tax
                        order.write({'sub_with_tax':values})
                        
