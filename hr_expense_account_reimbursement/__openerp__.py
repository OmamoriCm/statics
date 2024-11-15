# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Employee Expense Account - Reimbursement",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "version": "8.0.1.1.2",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "hr_expense_account",
        "hr_reimbursement",
    ],
    "data": [
        "views/hr_reimbursement_type_views.xml",
        "views/hr_reimbursement_views.xml",
        "views/hr_expense_account_views.xml",
    ],
    "demo": [],
}
