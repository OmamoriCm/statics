
from openerp import models, fields, api

class res_user(models.Model):
    _inherit = "res.users"

    stock_location = fields.Many2one('stock.location','WH Location',help="Warehouse Location")