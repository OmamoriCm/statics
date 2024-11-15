# -*- coding: utf-8 -*-

######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

from openerp.osv import osv, fields

class account_payment_preference(osv.osv):

    _description = 'Payment preference'
    _name = 'account.payment_preference'
    _order = 'name'

    _columns = {
        'name': fields.char('Option', size=64),
    }