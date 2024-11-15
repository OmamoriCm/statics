# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Email Dashboard Tile Value",
    "version": "8.0.2.0.0",
    "category": "web",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "email_template",
        "web_dashboard_tile_category",
    ],
    "data": [
        "views/tile_category_views.xml",
    ],
}
