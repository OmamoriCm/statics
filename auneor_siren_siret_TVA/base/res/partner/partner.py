# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _

class res_partner(osv.osv):
    _description = 'The partner object'
    _inherit = 'res.partner'
    _columns = {
        'siret': fields.char('Siret', size=14),
        'siren': fields.char('Siren', size=9, readonly=True),
        'rcs': fields.char('RCS', size=128),
    }

    def onchange_siret(self, cr, uid, ids, value):
        siren = ''
        if value and value.isdigit():
            if len(value) >= 9:
                siren = value[:9]
        return {'value':{'siren': siren}}

    def write(self, cr, uid, ids, vals, context={}):
        if 'siret' in vals: # If the field is modify
            if vals['siret']:
                if vals['siret'].isdigit() and len(vals['siret']) == 14:
                     vals['siren'] = vals['siret'][:9]
                else:
                    #raise osv.except_osv("Attention !!","Le nombre de chiffre du numéro de SIRET est incorrect.\nUn numéro SIRET contient 14 chiffres.")
                    raise osv.except_osv(_("The number of digit is wrong !"), _("The SIRET field must contains 14 digits."))
            else:
               vals['siren'] = ''
        return super(res_partner, self).write(cr, uid, ids, vals, context)

res_partner()
