# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class PartnerEvaluationTemplateItem(models.Model):
    _name = "partner.evaluation_template_item"
    _description = "Partner Evaluation Template Item"
    _order = "sequence, id"

    template_id = fields.Many2one(
        string="Partner Evaluation Template",
        comodel_name="partner.evaluation_template",
        required=True,
        ondelete="cascade",
    )
    item_type_id = fields.Many2one(
        string="Item Type",
        comodel_name="partner.evaluation_item_type",
        required=True,
        ondelete="restrict",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        required=True,
    )
