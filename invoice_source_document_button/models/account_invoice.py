# -*- coding: utf-8 -*-

from openerp import api, models, _
from openerp.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit='account.invoice'
    
    
    @api.multi
    def action_view_saleorder(self):
        so_id = self.env['sale.order'].search([('name', '=', self.origin)])
         
        action = self.env.ref('sale.action_quotations').read()[0]
        
        action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
        action['target'] = 'main'

        if len(so_id) == 1:
            action['res_id'] = so_id.id
            return action
        elif  len(so_id) > 1:
            action['views'] = [(self.env.ref('sale.view_quotation_tree').id, 'tree'),(self.env.ref('sale.view_order_form').id, 'form')]
            action['domain'] = [('id','in',so_id.ids)]
            return action
        else :
            raise ValidationError(_("No Sale Order for this customer invoice"))
    
    @api.multi
    def action_view_po(self):
        po_id = self.env['purchase.order'].search([('name', '=', self.origin)])
         
        action = self.env.ref('purchase.purchase_form_action').read()[0]
        action['target'] = 'main'
        
        if len(po_id) == 1:
            action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = po_id.id
            return action
        elif  len(so_id) > 1:
            action['views'] = [(self.env.ref('purchase.purchase_order_tree').id, 'tree'),(self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['domain'] = [('id','in',po_id.ids)]
            return action
        else :
            raise ValidationError(_("No Purchase Order for this vendor bill"))
            