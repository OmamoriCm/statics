# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Room Reservation",
    "version": "8.0.1.0.0",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "property_reservation_common",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/property_reservation_type_data.xml",
        "views/property_room_reservation_views.xml",
    ],
}
