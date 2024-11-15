# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class MeasurementItemType(models.Model):
    _name = "measurement.item_type"
    _description = "Measurement Item Type"

    name = fields.Char(
        string="Measurement Item Type",
        required=True,
    )
    code = fields.Char(
        string="Code",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    question_type = fields.Selection(
        string="Type",
        selection=[
            ("qualitative", "Qualitative"),
            ("quantitative", "Quantitative"),
        ],
        required=True,
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
    )
    qualitative_option_ids = fields.One2many(
        string="Qualitative Options",
        comodel_name="measurement.item_type_qualitative_option",
        inverse_name="type_id",
    )
