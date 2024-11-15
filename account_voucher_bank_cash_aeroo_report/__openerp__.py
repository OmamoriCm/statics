# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author/
{
    "name": "Account Voucher Bank Cash Report",
    "version": "8.0.1.0.0",
    "summary": "Account Voucher Bank Cash report",
    "category": "Accounting",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "website": "https://simetri-sinergi.id",
    "depends": [
        "account_voucher_bank_cash",
        "report_aeroo",
        "base_amount_to_text",
        "base_print_policy",
    ],
    "data": [
        "reports/report_account_voucher_bank_cash.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
    "license": "AGPL-3",
}
