# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2017  KnowledgeWare  (http://www.kware-eg.com)
#    All Rights Reserved.
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
    'name': 'PriceList Security',
    'version': '1.8.0',
    'category': 'Sales',
    'sequence': 12,
    'summary': '',
    'description': """
PriceList Security
================
It creates a many2many field between PriceLists and users. If you set Pricelists to User, then this PriceLists will be only seen by selected users.
This fields are only seen by users with "access right management"
    """,
    'author':  'KnowledgeWare',
    'website': 'www.kware-eg.com',
    'license': 'AGPL-3',
    'images': [
    ],
    'depends': [
        'base',
        'product',
    ],
    'data': [
            'res_users_view.xml',
            'pricelist_view.xml',
            'security/pricelist_security_security.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: