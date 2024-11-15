# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "HR Holiday Multiple Approval",
    "version": "8.0.1.0.1",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "auto_install": False,
    "depends": [
        "hr_holiday_notebook",
        "hr_holiday_configuration_page",
        "base_workflow_policy",
    ],
    "data": [
        "data/hr_holidays_workflow.xml",
        "data/base_workflow_policy_data.xml",
        "views/hr_holiday_config_setting_views.xml",
        "views/hr_holidays_view.xml",
        "views/hr_holidays_status_view.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
    "post_init_hook": "set_double_validation_false",
}
