# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Sale Utilities",
    "version": "8.0.1.1.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "category": "Sales Management",
    "depends": [
        "sale_stock",
        "sale_order_line_view",
    ],
    "data": [
        "security/res_partner_saleperson_rule.xml",
        "views/res_partner_view.xml",
        "views/sale_order_view.xml",
        "views/sale_order_line_view.xml",
    ],
    "installable": True,
}
