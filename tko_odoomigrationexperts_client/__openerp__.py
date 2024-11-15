# -*- coding: utf-8 -*-
{
    "name": "OdooMigrationExperts Client",
    "description": "Migrate any odoo version to any version with the token from OdooMigrationExperts",
    "category": "Server-Tools",
    "version": "8.0.0.1",
    "author": "OdooMigrationExperts",
    "license": "Other proprietary",
    "website": "https://https://odoomigrationexperts.com/",
    "support": "info@odoomigrationexperts.com",
    "depends": [
        'base_setup',
        'mail',
    ],
    "data": [
        'views/res_config.xml',
    ],
    "images": [
        'static/description/banner.png',
        ],
    "application": True,
    "installable": True,
    "auto_install": False,
}
