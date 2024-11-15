# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2010-2013 Elico Corp. All Rights Reserved.
#    Author: Yannick Gouin <yannick.gouin@elico-corp.com>
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
    'name': 'Global Discount on Sale Orders & Invoices',
    'version': '1.0',
    'license': 'AGPL-3',
    'category': 'Sales Management',
    'description': """
    Define global discount on whole Sale Order and Invoices. \n
    Also add Discount entry in the accounting Entry for Invoices.  
    """,
    'author': 'Vaibhav Bagal',
    'website': 'https://www.linkedin.com/in/vaibhav14b/',
    'depends': ['base', 'account', 'sale'],
    'init_xml': [],
    'data': ['sale_view.xml'],
    'images': ['static/description/main.jpg'],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: