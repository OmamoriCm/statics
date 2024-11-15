# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Direct Link From Lead/Opportunity To Quotation/Sale Order",
    "version": "8.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "sale_crm",
    ],
    "data": [
        "views/crm_lead_views.xml",
        "views/sale_order_views.xml",
    ],
}
