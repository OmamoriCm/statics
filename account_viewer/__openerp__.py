# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account viewer module for OpenERP
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
    'name': 'Account Viewer',
    'summary': """Adds a group 'Invoice & Payment viewer'""",
    'version': '1.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'description': """
Account Viewer
==============

This module adds a group *Invoice & Payment viewer* in the *Accounting & Finance* application. This group grants read-only access to invoices, refunds and payments. If you add a user to this new group, he should also be in the group *Human Ressources - Employee*.

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['account'],
    'data': [
        'security/account_security.xml',
        'security/ir.model.access.csv',
        'account_viewer_view.xml',
    ],
    'installable': True,
    'active': False,
}
