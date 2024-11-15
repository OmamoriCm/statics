# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class PartnerEvaluationResult(models.Model):
    _name = "partner.evaluation_result"
    _description = "Partner Evaluation Result"
    _order = "sequence, id"

    name = fields.Char(
        string="Result",
        required=True,
    )
    code = fields.Char(
        string="Code",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    quantitative_value = fields.Float(
        string="Quantitative Value",
        required=True,
        default=0.0,
    )
    template_id = fields.Many2one(
        string="Template",
        comodel_name="partner.evaluation_template",
        required=True,
        ondelete="cascade",
    )
    server_action_ids = fields.Many2many(
        string="Server Actions",
        comodel_name="ir.actions.server",
        relation="rel_partner_evaluation_result_2_server_act",
        column1="result_id",
        column2="action_id",
    )
    note = fields.Text(
        string="Note",
    )
