# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class MeasurementType(models.Model):
    _name = "measurement.type"
    _description = "Measurement Type"

    name = fields.Char(
        string="Measurement Type",
        required=True,
    )
    code = fields.Char(
        string="Code",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
    )
    note = fields.Text(
        string="Note",
    )
    measurement_confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm Measurement",
        comodel_name="res.groups",
        relation="rel_measurement_type_confirm_measurement",
        column1="type_id",
        column2="group_id",
    )
    measurement_approve_grp_ids = fields.Many2many(
        string="Allow To Approve Measurement",
        comodel_name="res.groups",
        relation="rel_measurement_type_approve_measurement",
        column1="type_id",
        column2="group_id",
    )
    measurement_start_grp_ids = fields.Many2many(
        string="Allow To Confirm Measurement",
        comodel_name="res.groups",
        relation="rel_measurement_type_start_measurement",
        column1="type_id",
        column2="group_id",
    )
    measurement_done_grp_ids = fields.Many2many(
        string="Allow To Finish Measurement",
        comodel_name="res.groups",
        relation="rel_measurement_type_done_measurement",
        column1="type_id",
        column2="group_id",
    )
    measurement_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel Measurement",
        comodel_name="res.groups",
        relation="rel_measurement_type_cancel_measurement",
        column1="type_id",
        column2="group_id",
    )
    measurement_restart_grp_ids = fields.Many2many(
        string="Allow To Restart Measurement",
        comodel_name="res.groups",
        relation="rel_measurement_type_restart_measurement",
        column1="type_id",
        column2="group_id",
    )
