# -*- coding: utf-8 -*-

from openerp import models, fields, api

class product_product(models.Model):
    _inherit = 'product.product'
    
    product_export_id = fields.Char(string='Product Export ID',readonly=False)
    
    def create(self, cr, uid, vals, context=None):

        if context is None:
            context = {}
        ctx = dict(context or {}, create_product_product=True)
        data = super(product_product, self).create(cr, uid, vals, context=ctx)

        related_vals = {}
        vals['product_export_id'] ='__export__.product_product_' + str(data)
        if vals.get('product_export_id'):
            related_vals['product_export_id'] = vals['product_export_id']
        if related_vals:
            self.write(cr, uid, data, related_vals, context=context)

        return data
