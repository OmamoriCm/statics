# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountMoveLine(models.Model):
    _name = "account.move.line"
    _inherit = "account.move.line"

    reimbursement_id = fields.Many2one(
        string="Reimbursement",
        comodel_name="hr.reimbursement",
        readonly=True,
    )
