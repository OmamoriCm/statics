# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResConfig(models.TransientModel):
    _name = "hr.holiday_config_setting"
    _inherit = "hr.holiday_config_setting"

    leave_request_confirm_grp_ids = fields.Many2many(
        string="Allowed To Confirm Leave Request",
        comodel_name="res.groups",
        related="company_id.leave_request_confirm_grp_ids",
    )
    leave_request_cancel_grp_ids = fields.Many2many(
        string="Allowed To Cancel Leave Request",
        comodel_name="res.groups",
        related="company_id.leave_request_cancel_grp_ids",
    )
    leave_request_restart_grp_ids = fields.Many2many(
        string="Allowed To Approve Leave Request",
        comodel_name="res.groups",
        related="company_id.leave_request_restart_grp_ids",
    )
    leave_request_restart_val_grp_ids = fields.Many2many(
        string="Allow To Restart Leave Request",
        comodel_name="res.groups",
        related="company_id.leave_request_restart_val_grp_ids",
    )
    leave_allocation_confirm_grp_ids = fields.Many2many(
        string="Allowed To Confirm Leave Allocation",
        comodel_name="res.groups",
        related="company_id.leave_allocation_confirm_grp_ids",
    )
    leave_allocation_cancel_grp_ids = fields.Many2many(
        string="Allowed To Cancel Leave Allocation",
        comodel_name="res.groups",
        related="company_id.leave_allocation_cancel_grp_ids",
    )
    leave_allocation_restart_grp_ids = fields.Many2many(
        string="Allowed To Approve Leave Allocation",
        comodel_name="res.groups",
        related="company_id.leave_allocation_restart_grp_ids",
    )
    leave_allocation_restart_val_grp_ids = fields.Many2many(
        string="Allow To Restart Leave Allocation",
        comodel_name="res.groups",
        related="company_id.leave_allocation_restart_val_grp_ids",
    )
