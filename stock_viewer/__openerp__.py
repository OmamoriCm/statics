# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock viewer module for OpenERP
#    Copyright (C) 2012-2014 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
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
    'name': 'Stock Viewer',
    'summary': """Adds a group 'Stock viewer'""",
    'version': '1.0',
    'category': 'Warehouse Management',
    'license': 'AGPL-3',
    'description': """
Stock Viewer
============

This module adds a group *Stock viewer* in the *Warehouse* application. This group grants read-only access to the Warehouse management. If you add a user to this new group, he should also be in the group *Human Ressources - Employee*.

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['stock'],
    'data': [
        'security/stock_security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'active': False,
}
