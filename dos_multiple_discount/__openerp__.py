# -*- coding: utf-8 -*-
##############################################################################
#
#    account_optimization module for OpenERP, Account Optimizations
#    Copyright (C) 2011 Alphasoft (<http://www.alphasoft.co.id)
#
#    account_optimization is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    account_optimization is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Multiple Product Discount",
    "version": "1.0",
    "license": "AGPL-3",
    'author': 'Alphasoft',
    'complexity': "easy",
    "category": "Sales",
    "description": """    
    This module aim to make multiple discount / discount plus plus on:
    * Product (Customer Discount base on Sales Price)
    * Sales Order
    * Integrate to Customer Invoice
    * Setting Partner Groups (Gold, Retail, Free)
    """,
    "website" : "http://www.alphasoft.co.id",
    "images" : [],
    'depends': ['base','product','sale','account'],
    'images': ['images/main_screenshot.png'],
    'init_xml': [
    ],
    'demo_xml': [
    ],
    'update_xml': [
        "security/discount_security.xml",
        "security/ir.model.access.csv",
        "partner_view.xml",
        "product_view.xml",
        "sale_view.xml",
        "invoice_view.xml",
    ],
    "init_xml": [],
    "demo_xml" : [],
    'test': [],
    'installable': True,
    #'application': True,
    'auto_install': False,
    'certificate': '',
    "css": [],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: