# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
{
    "name": "Use product supplier info for customers too",
    "version": "8.0.1.0.0",
    "author": "OdooMRP team,"
              "AvanzOSC,"
              "Serv. Tecnol. Avanzados - Pedro M. Baeza,"
              "Odoo Community Association (OCA)",
    "website": "http://www.odoomrp.com",
    "category": "Sales Management",
    "license": 'AGPL-3',
    "depends": [
        "base",
        "product",
    ],
    "data": [
        "views/product_view.xml",
    ],
    "demo": [
        "demo/product_demo.xml",
    ],
    "installable": True,
    "post_init_hook": "post_init_hook",
}
