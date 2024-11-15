# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Roberto Barreiro (<roberto@disgal.es>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv


class res_partner_working_time(osv.osv):
    _name = "res.partner.working.time"
    _columns = {
        'partner_id': fields.many2one('res.partner', 'Partner', ondelete='cascade', select=True, domain=['|',('is_company','=',True),('parent_id','=',False)]),
        'days': fields.char('Days'),
        'morning': fields.char('Morning'),
        'afternoon': fields.char('Afternoon'),
    }

class res_company(osv.osv):
    _inherit = "res.company"
    _columns = {
        'schedule': fields.one2many('res.partner.working.time', 'partner_id', 'Working Time'),
    }

class res_partner(osv.osv):
    _inherit = "res.partner"
    _columns = {
        'schedule': fields.one2many('res.partner.working.time', 'partner_id', 'Working Time'),
    }

