# -*- coding: utf-8 -*-
# Copyright 2018-2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Base Property Management",
    "version": "8.0.2.3.0",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/property_base.xml",
        "views/property_tenacy_status_views.xml",
        "views/property_availability_status_views.xml",
        "views/property_object_type_views.xml",
        "views/property_object_views.xml",
    ],
}
