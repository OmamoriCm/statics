# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class HrReimbursementType(models.Model):
    _name = "hr.reimbursement_type"
    _inherit = "hr.reimbursement_type"

    expense_account_ids = fields.Many2many(
        string="Expense Accounts",
        comodel_name="account.account",
        relation="rel_reimbursement_type_2_expense_account",
        column1="type_id",
        column2="account_id",
    )
