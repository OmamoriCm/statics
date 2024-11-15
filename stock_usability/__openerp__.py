# -*- coding: utf-8 -*-
##############################################################################
#
#    Stock Usability module for Odoo
#    Copyright (C) 2014-2015 Akretion (http://www.akretion.com)
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
    'name': 'Stock Usability',
    'version': '0.2',
    'category': 'Inventory, Logistic, Storage',
    'license': 'AGPL-3',
    'summary': 'Several usability enhancements in Warehouse management',
    'description': """
Stock Usability
===============

The usability enhancements include:
* display the source location on the tree view of the move lines of the pickings (by default, only the destination location is displayed).
* always display the field *Backorder* on the form view of picking (by default, this field is only displayed when it has a value, so the user doesn't know when the field has no value because he doesn't see the field !)
* add a group by Partner in the picking search view (particularly usefull for receptions)
* add graph view for pickings
* remove ability to translate stock.location, stock.location.route and stock.picking.type

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['stock'],
    'data': [
        'stock_view.xml',
        'procurement_view.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
}
