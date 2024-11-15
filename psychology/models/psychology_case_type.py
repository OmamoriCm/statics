# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class PsychologyCaseType(models.Model):
    _name = "psychology.case_type"
    _description = "Psychology Case Type"

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
    case_sequence_id = fields.Many2one(
        string="Case Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    # Service Related Fields
    service_sequence_id = fields.Many2one(
        string="Service Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    service_allowed_product_ids = fields.Many2many(
        string="Service Allowed Products",
        comodel_name="product.product",
        relation="rel_psychology_case_type_2_service_allowed_product",
        column1="type_id",
        column2="product_id",
    )
    service_allowed_product_categ_ids = fields.Many2many(
        string="Fix Item Allowed Product Categories",
        comodel_name="product.category",
        relation="rel_psychology_case_type_2_service_allowed_product_categ",
        column1="type_id",
        column2="product_id",
    )
    allowed_psychologist_ids = fields.Many2many(
        string="Allowed Psychologist",
        comodel_name="res.partner",
        relation="rel_psychology_case_type_allowed_psychologist",
        column1="type_id",
        column2="partner_id",
    )
    receivable_journal_id = fields.Many2one(
        string="Receivable Journal",
        comodel_name="account.journal",
        company_dependent=True,
    )
    receivable_account_id = fields.Many2one(
        string="Receivable Account",
        comodel_name="account.account",
        company_dependent=True,
    )
    service_pricelist_id = fields.Many2one(
        string="Service Pricelist",
        comodel_name="product.pricelist",
        company_dependent=True,
    )
    psychology_service_start_grp_ids = fields.Many2many(
        string="Allow To Start Psychology Service",
        comodel_name="res.groups",
        relation="rel_psychology_case_type_confirm_service",
        column1="type_id",
        column2="group_id",
    )
    psychology_service_finish_grp_ids = fields.Many2many(
        string="Allow To Finish Psychology Service",
        comodel_name="res.groups",
        relation="rel_psychology_case_type_finish_service",
        column1="type_id",
        column2="group_id",
    )
    psychology_service_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel Psychology Service",
        comodel_name="res.groups",
        relation="rel_psychology_case_type_cancel_service",
        column1="type_id",
        column2="group_id",
    )
    psychology_service_restart_grp_ids = fields.Many2many(
        string="Allow To Restart Psychology Service",
        comodel_name="res.groups",
        relation="rel_psychology_case_type_restart_service",
        column1="type_id",
        column2="group_id",
    )
    psychology_service_unlink_invoice_grp_ids = fields.Many2many(
        string="Allow To Delete Customer Invoice from Psychology Service",
        comodel_name="res.groups",
        relation="rel_psychology_case_type_out_invoice_service",
        column1="type_id",
        column2="group_id",
    )
    # Activity Related Field
    activity_sequence_id = fields.Many2one(
        string="Activity Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    activity_allowed_product_ids = fields.Many2many(
        string="Activity Allowed Products",
        comodel_name="product.product",
        relation="rel_psychology_case_type_2_activity_allowed_product",
        column1="type_id",
        column2="product_id",
    )
    activity_allowed_product_categ_ids = fields.Many2many(
        string="Activity Allowed Product Categories",
        comodel_name="product.category",
        relation="rel_psychology_case_type_2_activity_allowed_product_categ",
        column1="type_id",
        column2="product_id",
    )
    activity_pricelist_id = fields.Many2one(
        string="Activity Pricelist",
        comodel_name="product.pricelist",
        company_dependent=True,
    )
    psychology_activity_start_grp_ids = fields.Many2many(
        string="Allow To Start Psychology Activity",
        comodel_name="res.groups",
        relation="rel_psychology_case_type_confirm_activity",
        column1="type_id",
        column2="group_id",
    )
    psychology_activity_finish_grp_ids = fields.Many2many(
        string="Allow To Finish Psychology Activity",
        comodel_name="res.groups",
        relation="rel_psychology_case_type_finish_activity",
        column1="type_id",
        column2="group_id",
    )
    psychology_activity_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel Psychology Activity",
        comodel_name="res.groups",
        relation="rel_psychology_case_type_cancel_activity",
        column1="type_id",
        column2="group_id",
    )
    psychology_activity_restart_grp_ids = fields.Many2many(
        string="Allow To Restart Psychology Activity",
        comodel_name="res.groups",
        relation="rel_psychology_case_type_restart_activity",
        column1="type_id",
        column2="group_id",
    )
    psychology_activity_unlink_invoice_grp_ids = fields.Many2many(
        string="Allow To Delete Supplier Invoice from Psychology Activity",
        comodel_name="res.groups",
        relation="rel_psychology_case_type_in_invoice_activity",
        column1="type_id",
        column2="group_id",
    )
    # Case Workflow Policy Fields
    psychology_case_confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm Psychology Case",
        comodel_name="res.groups",
        relation="rel_psychology_case_type_confirm_case",
        column1="type_id",
        column2="group_id",
    )
    psychology_case_restart_approval_grp_ids = fields.Many2many(
        string="Allow To Restart Approval Psychology Case",
        comodel_name="res.groups",
        relation="rel_psychology_case_type_restart_approval_case",
        column1="type_id",
        column2="group_id",
    )
    psychology_case_start_grp_ids = fields.Many2many(
        string="Allow To Start Psychology Case",
        comodel_name="res.groups",
        relation="rel_psychology_case_type_start_case",
        column1="type_id",
        column2="group_id",
    )
    psychology_case_finish_grp_ids = fields.Many2many(
        string="Allow To Finish Psychology Case",
        comodel_name="res.groups",
        relation="rel_psychology_case_type_finish_case",
        column1="type_id",
        column2="group_id",
    )
    psychology_case_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel Psychology Case",
        comodel_name="res.groups",
        relation="rel_psychology_case_type_cancel_case",
        column1="type_id",
        column2="group_id",
    )
    psychology_case_restart_grp_ids = fields.Many2many(
        string="Allow To Restart Psychology Case",
        comodel_name="res.groups",
        relation="rel_psychology_case_type_restart_case",
        column1="type_id",
        column2="group_id",
    )
    psychology_case_out_invoice_grp_ids = fields.Many2many(
        string="Allow To Create Customer Invoice From Service",
        comodel_name="res.groups",
        relation="rel_psychology_case_type_out_invoice_case",
        column1="type_id",
        column2="group_id",
    )
    psychology_case_in_invoice_grp_ids = fields.Many2many(
        string="Allow To Create Supplier Invoice From Activity",
        comodel_name="res.groups",
        relation="rel_psychology_case_type_in_invoice_case",
        column1="type_id",
        column2="group_id",
    )
