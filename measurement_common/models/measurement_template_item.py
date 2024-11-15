# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class MeasurementTemplateItem(models.Model):
    _name = "measurement.template_item"
    _description = "Measurement Template Item"
    _order = "sequence, id"

    template_id = fields.Many2one(
        string="Measurement Template",
        comodel_name="measurement.template",
        required=True,
        ondelete="cascade",
    )
    item_type_id = fields.Many2one(
        string="Item Type",
        comodel_name="measurement.item_type",
        required=True,
        ondelete="restrict",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        required=True,
    )
