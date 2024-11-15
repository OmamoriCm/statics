# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class HrEmployee(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    employee_reimbursement_payable_account_id = fields.Many2one(
        string="Employee Reimbursement Payable Account",
        comodel_name="account.account",
        domain=[
            ("reconcile", "=", True),
        ],
        required=False,
    )
