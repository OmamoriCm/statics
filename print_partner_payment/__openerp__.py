# -*- encoding: utf-8 -*-

##############################################################################
#
#    Education module Odoo 8
#    Copyright (c) 2018 Copyright (c) 2018 aek
#      Anicet Eric Kouame <anicetkeric@gmail.com>
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
    'name': 'Payment receipt',
    'description': """
Use to manage invoice partner payment.
=================================================================================================
""",
    # Your information
    'author': 'Anicet Eric Kouame / Yoboue Parfait Alla / Hermann Kouadio',
    'website': '',
    'license': 'AGPL-3',
    'version': '8.0',
    "depends": ['base','account_voucher'],
    "category": "Accounting",
    'summary': 'Use to manage partner payment',
    'data': [
        "report/paper_format.xml",
        "report/received.xml",
        "report/report.xml",
        "views/views.xml",
    ],
    'images': [
        'images/cover.png'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
