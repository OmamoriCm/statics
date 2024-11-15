# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 BrowseInfo(<http://www.browseinfo.in>).
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
    'name': 'Employee Project Tasks',
    'version': '8.0.0.2',
    'author': 'BrowseInfo',
    "category": "Human Resources",
    "currency": "EUR",
    "price": 10,
    "description": """
        This module helps to display assinged task to Employee, employee tasks, tasks employee,visible tasks on employee. Tasks list on employee,
    """,
    'license':'AGPL-3',
    'summary': 'This module helps to display assinged task to Employee form and kanban view',
    'website': 'https://www.browseinfo.in',
    'description':""" """, 
    'depends':['base','hr','project'],
    'data':[
        'views/employee_task.xml',
        'security/employee_security.xml',
        ],
    'installable': True,
    'auto_install': False,
    "live_test_url":'https://youtu.be/hW7tdOYQrY4',
    "images":['static/description/Banner.png'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

