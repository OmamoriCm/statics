from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.exceptions import Warning

class webkul_pos_addons(osv.osv_memory):
    _name = 'webkul.pos.addons'
    _inherit = 'res.config.settings'

    _columns = {
        'module_pos_category_filter': fields.boolean(string="POS category filter"),
        'pos_cat_merge': fields.boolean(string="POS Category Merge"),

        'module_pos_product_pack':fields.boolean(string="POS product pack"),
        'module_pos_invoice':fields.boolean(string="POS invoice"),
        'module_pos_stocks':fields.boolean(string="POS stocks"),
        'module_pos_order_reprint':fields.boolean(string="POS order reprint"),
        'module_pos_discounted_product':fields.boolean(string="POS discounted product"),
        'module_pos_loyalty_management':fields.boolean(string="POS loyalty management"),
        'module_pos_coupons':fields.boolean(string="POS coupons"),
        'module_pos_carry_bag':fields.boolean(string="POS carry bag"),
        'module_pos_clock':fields.boolean(string="POS clock"),



    }
