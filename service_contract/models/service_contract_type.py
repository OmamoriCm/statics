# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ServiceContractType(models.Model):
    _name = "service.contract_type"
    _description = "Service Contract Type"

    name = fields.Char(
        string="Type",
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
    contract_sequence_id = fields.Many2one(
        string="Contract Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    contract_custom_info_template_id = fields.Many2one(
        string="Custom Info Template",
        comodel_name="custom.info.template",
    )
    team_function_allowed_product_ids = fields.Many2many(
        string="Team Function Allowed Products",
        comodel_name="product.product",
        relation="rel_contract_type_2_team_function_allowed_product",
        column1="type_id",
        column2="product_id",
    )
    team_function_allowed_product_categ_ids = fields.Many2many(
        string="Team Function Allowed Product Categories",
        comodel_name="product.category",
        relation="rel_contract_type_2_team_function_allowed_product_categ",
        column1="type_id",
        column2="product_id",
    )
    fix_item_allowed_product_ids = fields.Many2many(
        string="Fix Item Allowed Products",
        comodel_name="product.product",
        relation="rel_contract_type_2_fix_item_allowed_product",
        column1="type_id",
        column2="product_id",
    )
    fix_item_allowed_product_categ_ids = fields.Many2many(
        string="Fix Item Allowed Product Categories",
        comodel_name="product.category",
        relation="rel_contract_type_2_fix_item_allowed_product_categ",
        column1="type_id",
        column2="product_id",
    )
    fix_item_receivable_journal_id = fields.Many2one(
        string="Fix Item Receivable Journal",
        comodel_name="account.journal",
        company_dependent=True,
    )
    fix_item_receivable_account_id = fields.Many2one(
        string="Fix Item Receivable Account",
        comodel_name="account.account",
        company_dependent=True,
    )
    parent_analytic_account_id = fields.Many2one(
        string="Parent Analytic Account",
        comodel_name="account.analytic.account",
    )
    service_contract_confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm Contract",
        comodel_name="res.groups",
        relation="rel_contract_type_confirm_contract",
        column1="type_id",
        column2="group_id",
    )
    service_contract_restart_approval_grp_ids = fields.Many2many(
        string="Allow To Restart Approval Contract",
        comodel_name="res.groups",
        relation="rel_contract_type_restart_approval_contract",
        column1="type_id",
        column2="group_id",
    )
    service_contract_start_grp_ids = fields.Many2many(
        string="Allow To Force Start Contract",
        comodel_name="res.groups",
        relation="rel_contract_type_start_contract",
        column1="type_id",
        column2="group_id",
    )
    service_contract_finish_grp_ids = fields.Many2many(
        string="Allow To Force Finish Contract",
        comodel_name="res.groups",
        relation="rel_contract_type_finish_contract",
        column1="type_id",
        column2="group_id",
    )
    service_contract_terminate_grp_ids = fields.Many2many(
        string="Allow To Terminate Contract",
        comodel_name="res.groups",
        relation="rel_contract_type_terminate_contract",
        column1="type_id",
        column2="group_id",
    )
    service_contract_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel Contract",
        comodel_name="res.groups",
        relation="rel_contract_type_cancel_contract",
        column1="type_id",
        column2="group_id",
    )
    service_contract_restart_grp_ids = fields.Many2many(
        string="Allow To Restart Contract",
        comodel_name="res.groups",
        relation="rel_contract_type_restart_contract",
        column1="type_id",
        column2="group_id",
    )
