# Copyright 2017-2019 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Cheque Accounting Voucher",
    "version": "8.0.2.2.0",
    "category": "Accounting",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_voucher_bank_cash",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "data/account_voucher_type_data.xml",
        "data/ir_windows_action_data.xml",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_workflow_policy_cheque_payment_data.xml",
        "data/base_workflow_policy_cheque_receipt_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "views/account_cheque_voucher_views.xml",
        "views/account_cheque_receipt_views.xml",
        "views/account_cheque_payment_views.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
}
