# -*- encoding: utf-8 -*-

{
    'name': 'Export Data Tracking',
    'version': '0.1',
    'license': 'AGPL-3',
    'author': 'Tamkeen Technologies',
    'website': 'http://tamkeentech.sa/',
    'category': 'Web',
    'description': """
Export Data Tracking
###############################
- Enable the admin to grant the export option to specific users.    
- Create a log for the users who exported the data from the system and keep a log to the exported data for securing the export process.
""",
    'depends': ['web'],
    'data': [
        'security/export_group.xml',
        'security/ir.model.access.csv',
        'view/track_export_view.xml',
        'view/web_track_export_view.xml',
    ],
    'images': ['images/main_screenshot.png'],
    'auto_install': False,
}
