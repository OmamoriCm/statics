# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Service Contract - Recurring Service",
    "version": "8.0.1.9.0",
    "author": "PT. Simetri Sinergi Indonesia,OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "depends": [
        "service_contract",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/service_contract_type_views.xml",
        "views/service_contract_views.xml",
        "views/service_contract_recurring_period_views.xml",
    ],
    "demo": [
        "demo/product_category_demo.xml",
        "demo/product_demo.xml",
        "demo/service_contract_type_demo.xml",
    ],
    "installable": True,
}
