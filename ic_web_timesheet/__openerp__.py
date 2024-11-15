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


{
    'name': 'Web Timesheets Improvements',
    'version': '2.0',
    'category': 'Human Resources',
    'summary': 'Timesheets, Attendances, Activities',
    'description': """
Improve the timesheets application
==================================

This module improve the Odoo timesheet application by allowing:
---------------------------------------------------------------
 * The displaying of a month timesheet by week
 * The possibility to set an analytic account as read only 
 * The possibility to add comment directly with the summary view
 * The computation of the total of hours for the week and for the month

The day duration can be configured in the HR settings.
    """,
    'author': 'Idealis Consulting',
    'website': 'http://www.idealisconsulting.com',
    'images': ['images/timesheet.png'],
    'depends': ['hr_timesheet_sheet'],
    'data': [
        'res_config_view.xml',
        'analytic_account_view.xml',
        'views/ic_web_timesheet.xml',
    ],
    'qweb': ['static/src/xml/timesheet.xml'],
    'demo': [],
    'test':[],
    'installable': True,
    'auto_install': False,
    'application': False,
}

