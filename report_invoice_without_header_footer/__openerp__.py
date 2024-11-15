# -*- encoding: utf-8 -*-
##############################################################################
#
#     report for Odoo 8 custom
#    Copyright (c) 2018 Copyright (c) 2018 aek
#      Anicet Eric Kouame <anicetkeric@gmail.com>
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


{
    # Module information
    'name': 'Invoice Report without header footer',
    'version': '8.0.0.0.0',
    'category': 'Reports',
    'description': 'Add new option for generate invoice without header and footer.',
    'summary': 'Add new option for generate invoice without header and footer.',

    # Your information
    'author': 'Anicet Eric Kouame',
    'website': 'https://github.com/anicetkeric',
    'license': 'AGPL-3',

    'images': [
        'images/banner.png'
    ],

    # Dependencies
    'depends': ['base', 'report', 'account'],

    # Views templates, pages, menus, options and snippets
    'data': [
        'views/report_custom.xml',
        'reports/reports.xml',
    ],
    # Technical options
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
