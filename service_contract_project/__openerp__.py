# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Service Contract Integration With Project Management",
    "version": "8.0.1.1.1",
    "author": "PT. Simetri Sinergi Indonesia,OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "license": "AGPL-3",
    "depends": [
        "project",
        "service_contract",
    ],
    "data": [
        "views/service_contract_views.xml",
        "views/service_contract_type_views.xml",
    ],
    "demo": [
        "demo/service_contract_type_demo.xml",
    ],
    "installable": True,
}
