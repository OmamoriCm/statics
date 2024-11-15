# -*- coding: utf-8 -*-

######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

from openerp.osv import osv, fields

class res_partner(osv.osv):

    _inherit = 'res.partner'

    _columns = {
        'account_payment_preference':fields.many2one('account.payment_preference','Payment Preference',select=True),
    }
