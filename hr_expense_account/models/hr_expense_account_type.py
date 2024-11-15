# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class HrExpenseAccountType(models.Model):
    _name = "hr.expense_account_type"
    _description = "Employee Expense Account Type"

    name = fields.Char(
        string="Expense Account Type",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        company_dependent=True,
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm",
        comodel_name="res.groups",
        relation="rel_confirm_exp_acc",
        column1="type_id",
        column2="group_id",
    )
    restart_approval_grp_ids = fields.Many2many(
        string="Allow To Restart",
        comodel_name="res.groups",
        relation="rel_restart_approval_exp_acc",
        column1="type_id",
        column2="group_id",
    )
    cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel",
        comodel_name="res.groups",
        relation="rel_cancel_exp_acc",
        column1="type_id",
        column2="group_id",
    )
    terminate_grp_ids = fields.Many2many(
        string="Allow To Terminate",
        comodel_name="res.groups",
        relation="rel_terminate_exp_acc",
        column1="type_id",
        column2="group_id",
    )
    restart_grp_ids = fields.Many2many(
        string="Allow To Restart",
        comodel_name="res.groups",
        relation="rel_restart_exp_acc",
        column1="type_id",
        column2="group_id",
    )
