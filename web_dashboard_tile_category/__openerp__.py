# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Web Tile Dashboard Category",
    "version": "8.0.1.2.0",
    "category": "web",
    "website": "https://opensynergy-indonesia.com/",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "web_dashboard_tile",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/tile_category_views.xml",
        "menu.xml",
    ],
}
