# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2018 8Bits Software
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
    'name': 'HR Employee Cam',
    'description': 'Enable employee take a photo from webcam',
    'summary': '''
        Enable in other menu in employee form a menu to take a photo
    ''',
    'version': '8.0.0.1',
    'author': '8Bits Software',
    'depends': [
        'base',
        'web',
        'hr'
    ],
    'data': [
        'hr_employee_cam.xml'
    ],
    'qweb': [
        'static/src/xml/*.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
