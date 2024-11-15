# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Common Measurement Feature",
    "version": "8.0.1.3.0",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "base_sequence_configurator",
        "base_workflow_policy",
        "base_cancel_reason",
        "base_print_policy",
        "mail",
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "wizards/start_measurement.xml",
        "wizards/end_measurement.xml",
        "views/measurement_type_views.xml",
        "views/measurement_item_type_views.xml",
        "views/measurement_template_views.xml",
        "views/measurement_common_views.xml",
    ],
}
