# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Partner's Management Application",
    "version": "8.0.2.0.1",
    "summary": "Base module to manage partner",
    "category": "Partner",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "base",
    ],
    "data": [
        "security/res_groups.xml",
        "menu.xml",
        "views/res_country_views.xml",
        "views/res_country_group_views.xml",
        "views/res_country_state_views.xml",
        "views/res_partner_category_views.xml",
        "views/res_partner_title_views.xml",
        "views/res_partner_bank_views.xml",
        "views/res_bank_views.xml",
        "views/res_partner_bank_type_views.xml",
        "views/res_partner_view.xml",
    ],
}
