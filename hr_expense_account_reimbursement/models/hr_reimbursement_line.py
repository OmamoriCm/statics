# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class HrReimbursementLine(models.Model):
    _name = "hr.reimbursement_line"
    _inherit = "hr.reimbursement_line"

    require_expense_account = fields.Boolean(
        string="Require Expense Account",
        readonly=True,
    )
    expense_account_id = fields.Many2one(
        string="Expense Account",
        comodel_name="hr.expense_account",
        readonly=True,
    )

    @api.multi
    def _check_expense_account(self):
        self.ensure_one()
        result = True
        if self.require_expense_account:
            if not self.expense_account_id:
                error_msg = _("No expense account")
                raise UserError(error_msg)

            if self.expense_account_id.amount_residual < 0.0:
                error_msg = _("Insuficient expense account")
                raise UserError(error_msg)
        return result

    @api.onchange(
        "type_id",
        "account_id",
    )
    def onchange_require_expense_account(self):
        self.onchange_require_expense_account = False
        if self.account_id and self.type_id:
            if self.account_id.id in self.type_id.expense_account_ids.ids:
                self.require_expense_account = True

    @api.onchange(
        "require_expense_account",
        "account_id",
        "product_id",
    )
    def onchange_expense_account_id(self):
        expense_account = False
        obj_expense_acc = self.env["hr.expense_account"]
        if self.require_expense_account:
            criteria = [
                ("employee_id", "=", self.employee_id.id),
                ("type_id.account_id", "=", self.account_id.id),
                ("state", "=", "approve"),
                ("date_assign", "<=", self.reimbursement_id.date_expense),
                "|",
                ("date_expire", "=", False),
                ("date_expire", ">=", self.reimbursement_id.date_expense),
            ]
            expense_accounts = obj_expense_acc.search(criteria)
            if len(expense_accounts) > 0:
                expense_account = expense_accounts[0]
        self.expense_account_id = expense_account
