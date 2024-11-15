# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Giro Accounting Voucher Analytic Plan Feature",
    "version": "8.0.1.0.1",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
    "depends": ["account_voucher_giro", "account_voucher_common_analytic_plan"],
    "data": [
        "views/account_giro_receipt_views.xml",
        "views/account_giro_payment_views.xml",
    ],
}