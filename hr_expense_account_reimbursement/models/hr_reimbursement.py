# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class HrReimbursement(models.Model):
    _name = "hr.reimbursement"
    _inherit = "hr.reimbursement"

    @api.multi
    def action_confirm(self):
        for record in self:
            record._check_expense_account()

        _super = super(HrReimbursement, self)
        _super.action_confirm()

    @api.multi
    def _check_expense_account(self):
        self.ensure_one()
        for line in self.line_ids:
            line._check_expense_account()

        return True

    @api.multi
    def action_reload_expense_account(self):
        for record in self:
            record._reload_expense_account()

    @api.multi
    def _reload_expense_account(self):
        self.ensure_one()
        for line in self.line_ids:
            line.onchange_require_expense_account()
            line.onchange_expense_account_id()
