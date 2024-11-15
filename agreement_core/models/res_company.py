# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    # Agreement Policy
    agreement_confirm_group_ids = fields.Many2many(
        string="Allow To Confirm Agreement",
        comodel_name="res.groups",
        relation="rel_company_agreement_allowed_confirm",
        column1="company_id",
        column2="group_id",
    )
    agreement_print_group_ids = fields.Many2many(
        string="Allow To Print Agreement",
        comodel_name="res.groups",
        relation="rel_company_agreement_allowed_print",
        column1="company_id",
        column2="group_id",
    )
    agreement_attach_group_ids = fields.Many2many(
        string="Allow To Attach Signed Document",
        comodel_name="res.groups",
        relation="rel_company_agreement_allowed_attach",
        column1="company_id",
        column2="group_id",
    )
    agreement_approve_group_ids = fields.Many2many(
        string="Allow To Approve Agreement",
        comodel_name="res.groups",
        relation="rel_company_agreement_allowed_approve",
        column1="company_id",
        column2="group_id",
    )
    agreement_active_group_ids = fields.Many2many(
        string="Allow To Activate Agreement",
        comodel_name="res.groups",
        relation="rel_company_agreement_allowed_active",
        column1="company_id",
        column2="group_id",
    )
    agreement_expire_group_ids = fields.Many2many(
        string="Allow To Mark As Expire Agreement",
        comodel_name="res.groups",
        relation="rel_company_agreement_allowed_expire",
        column1="company_id",
        column2="group_id",
    )
    agreement_terminate_group_ids = fields.Many2many(
        string="Allow To Terminate Agreement",
        comodel_name="res.groups",
        relation="rel_company_agreement_allowed_terminate",
        column1="company_id",
        column2="group_id",
    )
    agreement_revision_group_ids = fields.Many2many(
        string="Allow To Create New Revision",
        comodel_name="res.groups",
        relation="rel_company_agreement_allowed_revision",
        column1="company_id",
        column2="group_id",
    )
    agreement_cancel_group_ids = fields.Many2many(
        string="Allow To Cancel Agreement",
        comodel_name="res.groups",
        relation="rel_company_agreement_allowed_cancel",
        column1="company_id",
        column2="group_id",
    )
    agreement_restart_group_ids = fields.Many2many(
        string="Allow To Restart Agreement",
        comodel_name="res.groups",
        relation="rel_company_agreement_allowed_restart",
        column1="company_id",
        column2="group_id",
    )
