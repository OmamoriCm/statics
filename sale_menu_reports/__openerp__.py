# -*- coding:utf-8 -*-
#
#
#    Copyright (C) 2016 Sucros Clear Information Technologies PLC.
#    All Rights Reserved.
#       @author: Michael Telahun Makonnen <miket@clearict.com>
#
#    This program is free software: you can redistribute it and/or modify it
#    under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

{
    'name': 'Sales Reporting Menu',
    'summary': 'Move sales reporting menu items under Sales menu',
    'description': """
Moves the sales reports usually found in the 'Reporting' top-level menu to
the 'Sales' top-level menu.
    """,
    'author': 'Sucros Clear Information Technologies PLC',
    'website': 'http://clearict.com',
    'category': 'Sales',
    'version': '1.0',
    'depends': [
        'sale',
        'sales_team',
    ],
    'data': [
        'views/menu.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'active': False,
}
