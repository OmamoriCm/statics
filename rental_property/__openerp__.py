# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Rental Property",
    "version": "8.0.2.1.0",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "rental_common",
        "property_base"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/rental_property_type_data.xml",
        "data/base_workflow_policy_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "data/ir_cron_data.xml",
        "menu.xml",
        "views/rental_property_views.xml",
        "views/rental_property_detail_views.xml",
        "views/rental_property_detail_schedule_views.xml",
        "views/property_object_views.xml",
    ],
}
