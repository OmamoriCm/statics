# -*- coding: utf-8 -*-
##############################################################################
#
# This module is developed by Idealis Consulting SPRL
# Copyright (C) 2014 Idealis Consulting SPRL (<http://idealisconsulting.com>).
# All Rights Reserved
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv

class ic_timesheet_settings(osv.osv_memory):
    _inherit = 'hr.config.settings'

    _columns = {
        'timesheet_day_duration': fields.float('Timesheet day duration (in hours)', help='Expected day duration in hours in the timesheet.'),
    }

    def get_default_timesheet_day_duration(self, cr, uid, fields, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        return {
            'timesheet_day_duration': user.company_id.timesheet_day_duration,
        }

    def set_default_timesheet_day_duration(self, cr, uid, ids, context=None):
        config = self.browse(cr, uid, ids[0], context=context)
        user = self.pool.get('res.users').browse(cr, uid, uid, context)
        user.company_id.write({
            'timesheet_day_duration': config.timesheet_day_duration,
        })
