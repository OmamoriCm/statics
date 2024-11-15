# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Elmatica AS
#    Written by Tinderbox AS and Bringsvor Consulting AS
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
    'name': 'Currency Lookup',
    'version': '1.1',
    'author': 'Bringsvor Consulting AS',
    'website': 'http://www.bringsvor.com',
    'category': 'Utilities',
    'description': """
    Utility to do currency conversion by looking up the currency date tables of Odoo.

    Written by Bringsvor Consulting AS (www.bringsvor.com / bringsvor@bringsvor.com)
""",
    'depends': ['base', 'account'],
    'data': [
        'wizards/currency_lookup.xml',
    ],
    'demo': [],
    'test': [
        ],
    'installable': True,
    'auto_install': False,
}


