# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class PartnerEvaluationItem(models.Model):
    _name = "partner.evaluation_item"
    _description = "Partner Evaluation Item"

    @api.multi
    def _compute_allowed_qualitative_option_ids(self):
        obj_option = self.env["partner.evaluation_item_type_qualitative_option"]
        for document in self:
            result = []
            if document.item_type_id:
                criteria = [
                    ("type_id", "=", document.item_type_id.id),
                ]
                result = obj_option.search(criteria).ids
            document.allowed_qualitative_option_ids = result

    @api.multi
    @api.depends(
        "quantitative_value",
        "qualitative_option_id",
        "uom_id",
        "question_type",
    )
    def _compute_answer_string(self):
        for document in self:
            answer = ""
            if document.question_type == "qualitative":
                if document.qualitative_option_id:
                    answer = document.qualitative_option_id.name
            else:
                answer = "{} {}".format(
                    document.quantitative_value, document.uom_id.name
                )
            document.answer_string = answer

    @api.multi
    @api.depends(
        "item_type_id",
    )
    def _compute_method(self):
        for document in self:
            document.method = document.item_type_id.method

    evaluation_id = fields.Many2one(
        string="# Evaluation",
        comodel_name="partner.evaluation",
        required=True,
    )
    date_answer = fields.Datetime(
        string="Date",
    )
    item_type_id = fields.Many2one(
        string="Item",
        comodel_name="partner.evaluation_item_type",
        required=True,
    )
    method = fields.Selection(
        string="Method",
        selection=[
            ("manual", "Manual"),
            ("automatic", "Automatic"),
        ],
        compute="_compute_method",
        store=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        required=True,
    )
    question_type = fields.Selection(
        string="Type",
        selection=[
            ("qualitative", "Qualitative"),
            ("quantitative", "Quantitative"),
        ],
        required=True,
    )
    answer_string = fields.Char(
        string="Answer",
        compute="_compute_answer_string",
        store=False,
    )
    quantitative_value = fields.Float(
        string="Quantitative Value",
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
    )
    qualitative_option_id = fields.Many2one(
        string="Qualitative Value",
        comodel_name="partner.evaluation_item_type_qualitative_option",
    )
    allowed_qualitative_option_ids = fields.Many2many(
        string="Qualitative Options",
        comodel_name="partner.evaluation_item_type_qualitative_option",
        compute="_compute_allowed_qualitative_option_ids",
        store=False,
    )

    @api.multi
    def _compute_automatic_field(self):
        self.ensure_one()
        result = self.item_type_id._get_result(self)
        if self.question_type == "qualitative":
            self.write({"qualitative_option_id": result})
        else:
            self.write({"quantitative_value": result})
