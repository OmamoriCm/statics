# -*- coding: utf-8 -*-

######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

from openerp.osv import osv, fields
import logging

_logger = logging.getLogger(__name__)

class account_voucher(osv.osv):

    _inherit = 'account.voucher'

    _columns = {
	    'account_payment_preference':fields.many2one('account.payment_preference','Payment Preference',select=True),
    }

    def onchange_partner_id(self, cr, uid, ids, partner_id,\
	                        journal_id, amount, currency_id, \
							ttype, date, context=None):

        result = super(account_voucher, self).onchange_partner_id(cr, uid, ids, partner_id, journal_id, amount, currency_id, ttype, date, context=context)

        if not result:
            return result
		
        if partner_id:
            account_payment_preference = self.pool.get('res.partner').browse(cr, uid, partner_id).account_payment_preference
            result['value']['account_payment_preference'] = account_payment_preference and account_payment_preference.id or False
	return result
                                                


