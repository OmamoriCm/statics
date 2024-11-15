# -*- coding: utf-8 -*-

######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

from openerp.osv import osv, fields

class account_invoice(osv.osv):

    _inherit = 'account.invoice'

    _columns = {
	    'account_payment_preference':fields.many2one('account.payment_preference','Payment Preference',select=True),
    }

    def onchange_partner_id(self, cr, uid, ids, type, partner_id,\
                            date_invoice=False, payment_term=False, \
							partner_bank_id=False, company_id=False, context=None):
							
        result = super(account_invoice, self).onchange_partner_id(cr, uid, ids, type, partner_id, date_invoice, payment_term, partner_bank_id, company_id, context=context)
		
        if partner_id:
            account_payment_preference = self.pool.get('res.partner').browse(cr, uid, partner_id).account_payment_preference
            result['value']['account_payment_preference'] = account_payment_preference and account_payment_preference.id or False
	return result

