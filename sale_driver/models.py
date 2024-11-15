from openerp import fields, models, api


class account_invoice(models.Model):
    _name = "account.invoice"
    _inherit = ['account.invoice']

    driver_id = fields.Many2one('res.users', 'Driver')


class sale_order(models.Model):
    _name = "sale.order"
    _inherit = ['sale.order']

    driver_id = fields.Many2one('res.users', 'Driver')
    
    def _prepare_invoice(self, cr, uid, order, lines, context=None):
    	invoice_vals = super(sale_order, self)._prepare_invoice(
    		cr, uid, order, lines, context=None)
    	invoice_vals['driver_id'] = order.driver_id and order.driver_id.id or False
    	return invoice_vals
