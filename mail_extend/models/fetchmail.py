from openerp.osv import osv

class fetchmail_server(osv.osv):
    _name = 'fetchmail.server'
    _inherit = 'fetchmail.server'
    
    def fetch_mails(self, cr, uid, ids=False, context=None):
        return super(fetchmail_server,self)._fetch_mails(cr, uid, ids=ids, context=context)