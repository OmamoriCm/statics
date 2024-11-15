from openerp.osv import osv, fields, expression

class res_partner_group(osv.osv):
    _name = 'res.partner.group'
    _order = 'sequence'
    _columns = {
        'sequence' : fields.integer('Sequence'),
        'name' : fields.char('Name', required=True),
    }

class res_partner(osv.osv):
    _inherit = "res.partner"
    _description = "Partner"
    _columns = {
        'partner_group_id': fields.many2one('res.partner.group', 'Groups', select=True),
    }