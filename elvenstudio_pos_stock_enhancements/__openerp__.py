# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: ElvenStudio
#    Copyright 2015 elvenstudio.it
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
    'name': 'POS Stock enhancements',
    'category': 'Point of sale',
    'summary': 'POS stock enhancements',
    'version': '8.0.1.0.0',
    'author': 'Elvenstudio',
    'license': 'AGPL-3',
    'website': 'http://www.elvenstudio.it',
    'support': 'info@elvenstudio.it',

    'images': [
        'static/description/banner.jpg'
    ],

    'depends': [
        'point_of_sale',
    ],

    'data': [
        'views/point_of_sale_view.xml',
    ],

    'installable': True,
    'application': False,
}
