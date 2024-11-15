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

{
    'name': 'Working Time',
    'version': '8.0.2.2',
    'category': 'Website',
    'sequence': 10,
    'summary': 'Show your working time on contact form. It also manages partners working time',
    'description': """
    Manage working time of your partners.
    Show your own working time on website contact form.
    """,
    'author': 'Roberto Barreiro',
    'website': 'https://bitbucket.org/disgalmilladoiro/',
    'depends': ['website_crm',],
    'data': ['views/working_time_form.xml',
             'views/working_time.xml',],
    'images': ['static/description/banner.png',],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
