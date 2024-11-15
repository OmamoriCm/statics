# -*- coding: utf-8 -*-

{
    'name': 'Google Maps',
    'version': '8.0.1.0.0',
    'category': 'Extra Tools',
    'description': """This module adds a Map button on the partner’s form in order to open its address directly in the Google Maps""",
    'author': 'Ubaid ur Rehman <ubaidur.rehman018@yahoo.com>',
    'depends': ['base'],
    'init_xml': [],
    'images': ['images/google_map.png'],
    'data': [
            'views/google_map_view.xml',
            ],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
}