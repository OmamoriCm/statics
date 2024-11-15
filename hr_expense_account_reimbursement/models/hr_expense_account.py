# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class HrExpenseAccount(models.Model):
    _name = "hr.expense_account"
    _inherit = "hr.expense_account"

    @api.depends(
        "reimbursement_line_ids",
        "reimbursement_line_ids.price_subtotal",
        "reimbursement_line_ids.reimbursement_id.state",
    )
    def _compute_amount_reimbursement(self):
        for record in self:
            result = 0.0
            for line in record.reimbursement_line_ids:
                result += line.price_subtotal
            record.amount_reimbursement = result

    @api.depends(
        "amount_limit",
        "amount_reimbursement",
    )
    def _compute_amount(self):
        for record in self:
            amount_residual = 0.0
            amount_realize = record.amount_reimbursement
            record.amount_realize = amount_realize
            amount_residual = record.amount_limit - amount_realize
            record.amount_residual = amount_residual

    reimbursement_line_ids = fields.One2many(
        string="Reimbursement Lines",
        comodel_name="hr.reimbursement_line",
        inverse_name="expense_account_id",
        domain=[("reimbursement_id.state", "not in", ["cancel", "terminate"])],
        readonly=True,
    )
    amount_reimbursement = fields.Float(
        string="Amount Reimbursement",
        compute="_compute_amount_reimbursement",
        store=True,
    )
    amount_realize = fields.Float(
        compute="_compute_amount",
        store=True,
    )
    amount_residual = fields.Float(
        compute="_compute_amount",
        store=True,
    )

    @api.multi
    def _pre_cancel_check_10_reimbursement_line(self):
        self.ensure_one()
        if len(self.reimbursement_line_ids) > 0:
            error_msg = _("Expense account already use")
            raise UserError(error_msg)
