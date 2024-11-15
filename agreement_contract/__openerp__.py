# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Agreement - Contract",
    "version": "8.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "agreement_core",
        "account_analytic_analysis",
    ],
    "data": [
        "security/res_groups_data.xml",
        "views/agreement_agreement_views.xml",
        "views/account_analytic_account_views.xml",
    ],
}
