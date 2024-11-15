# -*- coding: utf-8 -*-
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp import models, fields, api
import dateutil.parser
import datetime


class sales_custom_module(models.Model):
    _inherit = 'sale.order.line'

    custom_checkbox = fields.Boolean(string="Custom")


class Sale(models.Model):
    _inherit = 'sale.order'

    color = fields.Char(default='yellow')
    custom_checkbox_order = fields.Boolean(string="Custom")
    is_sale_order = fields.Boolean(string="Is Sale Order")
    mrp_order_count = fields.Integer(
        'MRP Count', compute='_compute_mrp_order_count')

    mrp_order_ids = fields.One2many(
        'mrp.production', 'sale_order_id', string='MRP Order')

    @api.one
    @api.depends('mrp_order_ids')
    def _compute_mrp_order_count(self):
        self.mrp_order_count = len(self.mrp_order_ids)

    @api.multi
    def action_view_mrp_order(self):
        order_ids = self.mapped('mrp_order_ids')
        action = self.env.ref('mrp.mrp_production_action').read()[0]
        if len(order_ids) > 1:
            action['domain'] = [('id', 'in', order_ids)]
        elif len(order_ids) == 1:
            action['views'] = [
                (self.env.ref('mrp.mrp_production_form_view').id, 'form')]
            action['res_id'] = order_ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.model
    @api.onchange('order_line')
    def custom_field_checkbox(self):
        for order in self.order_line:
            if order.custom_checkbox == True:
                self.custom_checkbox_order = True
                break
            else:
                self.custom_checkbox_order = False

    @api.multi
    def get_products(self):
        order_id = []
        for order in self:
            for each_order in order.order_line:

                if each_order.product_id.type != 'service':
                    not_created = []
                    bom_obj = self.pool.get('mrp.bom')
                    bom_id = bom_obj._bom_find(
                        self.env.cr, self.env.uid, product_id=each_order.product_id.id, properties=[], context={})
                    res = {}
                    state = "confirmed"
                    details = self.env['mrp.production'].create({'product_id': each_order.product_id.id,
                                                                 'product_uom': each_order.product_uom.id,
                                                                 'product_qty': each_order.product_uom_qty,
                                                                 'bom_id': bom_id,
                                                                 'sale_order_id': each_order.order_id.id,
                                                                 'origin': order.name,
                                                                 })
                    if bom_id:
                        details.signal_workflow('button_confirm')
                        details.action_assign()
                    order_id.append(details.id)
        action = self.env.ref('mrp.mrp_production_action').read()[0]
        if len(order_id) > 1:
            action['domain'] = [('id', 'in', order_id)]
        elif len(order_id) == 1:
            action['views'] = [
                (self.env.ref('mrp.mrp_production_form_view').id, 'form')]
            action['res_id'] = order_id[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action


class Sale(models.Model):
    _inherit = 'mrp.production'

    sale_order_id = fields.Many2one(
        'sale.order', string='Sale Order', required=False)
