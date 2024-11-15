# -*- coding: utf-8 -*-
##############################################################################
#
#    Sale viewer module for Odoo
#    Copyright (C) 2012-2015 Akretion (http://www.akretion.com)
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
    'name': 'Sale Viewer',
    'summary': """Adds a group 'Sale viewer'""",
    'version': '1.0',
    'category': 'Sales Management',
    'license': 'AGPL-3',
    'description': """
Sale Viewer
===========

This module adds a group *Sale viewer* in the *Sales* application. This group grants read-only access to Sales Management. If you add a user to this new group, he should also be in the group *Human Ressources - Employee*.

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale'],
    'data': [
        'security/sale_security.xml',
        'security/ir.model.access.csv',
        'sale_view.xml',
    ],
    'installable': True,
}
