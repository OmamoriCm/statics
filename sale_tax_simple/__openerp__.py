# -*- coding: utf-8 -*-
{
    'name': 'Simple Sale Tax',
    'summary': 'Simple Sale Tax modification',
    'description': """
    Add a simple way to set or modify sale line taxes based on a filed.
     """,
    'version': '8.0.1.0',
    'category': 'Sale',
    'author': 'DVIT.me',
    'website': 'http://dvit.me',
    'license': 'AGPL-3',
    'depends': [
        'account','sale'
    ],
    'data': ['templates.xml'],
    'installable': True,
    'auto_install': False,
    'application': False,

}
