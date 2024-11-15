# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class HrReimbursementType(models.Model):
    _name = "hr.reimbursement_type"
    _description = "Employee Reimbursement Type"

    name = fields.Char(
        string="Employee Reimbursement Type",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        relation="rel_reimbursement_type_2_product_categ",
        column1="type_id",
        column2="category_id",
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Products",
        comodel_name="product.product",
        relation="rel_reimbursement_type_2_product",
        column1="type_id",
        column2="product_id",
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        company_dependent=True,
        domain=[
            ("type", "=", "general"),
        ],
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    employee_reimbursement_payable_account_id = fields.Many2one(
        string="Payable Account",
        comodel_name="account.account",
        company_dependent=True,
        domain=[
            ("reconcile", "=", True),
        ],
        required=True,
    )
    reimbursement_confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm Reimbursement",
        comodel_name="res.groups",
        relation="rel_reimbursement_type_confirm_reimbursement",
        column1="type_id",
        column2="group_id",
    )
    reimbursement_restart_approval_grp_ids = fields.Many2many(
        string="Allow To Restart Reimbursement Approval",
        comodel_name="res.groups",
        relation="rel_reimbursement_type_restart_approval_reimbursement",
        column1="type_id",
        column2="group_id",
    )
    reimbursement_change_detail_grp_ids = fields.Many2many(
        string="Allow To Change Reimbursement Detail",
        comodel_name="res.groups",
        relation="rel_reimbursement_type_change_detail_reimbursement",
        column1="type_id",
        column2="group_id",
    )
    reimbursement_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel Reimbursement",
        comodel_name="res.groups",
        relation="rel_reimbursement_type_cancel_reimbursement",
        column1="type_id",
        column2="group_id",
    )
    reimbursement_terminate_grp_ids = fields.Many2many(
        string="Allow To Terminate Reimbursement",
        comodel_name="res.groups",
        relation="rel_reimbursement_type_terminate_reimbursement",
        column1="type_id",
        column2="group_id",
    )
    reimbursement_restart_grp_ids = fields.Many2many(
        string="Allow To Restart Reimbursement",
        comodel_name="res.groups",
        relation="rel_reimbursement_type_restart_reimbursement",
        column1="type_id",
        column2="group_id",
    )
