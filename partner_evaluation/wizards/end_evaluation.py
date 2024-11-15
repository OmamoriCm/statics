# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class PartnerEndEvaluation(models.TransientModel):
    _name = "partner.end_evaluation"
    _description = "End Partner Evaluation"

    @api.model
    def _default_date_end(self):
        return fields.Datetime.now()

    @api.model
    def _default_evaluation_id(self):
        return self.env.context.get("active_id", False)

    @api.multi
    @api.depends(
        "evaluation_id",
    )
    def _compute_allowed_result_ids(self):
        for document in self:
            result = []
            if document.evaluation_id:
                template = document.evaluation_id.template_id
                for option in template.result_ids:
                    result.append(option.id)
            document.allowed_result_ids = result

    @api.multi
    @api.depends(
        "evaluation_id",
    )
    def _compute_manual_result(self):
        for document in self:
            document.manual_result = document.evaluation_id.template_id.manual_result

    evaluation_id = fields.Many2one(
        string="# Evaluation",
        comodel_name="partner.evaluation",
        default=lambda self: self._default_evaluation_id(),
    )
    manual_result = fields.Boolean(
        string="Manual Result",
        compute="_compute_manual_result",
        store=False,
    )
    result_id = fields.Many2one(
        string="Result",
        comodel_name="partner.evaluation_result",
    )
    allowed_result_ids = fields.Many2many(
        string="Allowed Results",
        comodel_name="partner.evaluation_result",
        compute="_compute_allowed_result_ids",
        store=False,
    )

    date_end = fields.Datetime(
        string="Date End",
        required=True,
        default=lambda self: self._default_date_end(),
    )

    @api.multi
    def action_end(self):
        self.ensure_one()
        obj_evaluation = self.env["partner.evaluation"]
        evaluation_ids = self._context.get("active_ids", [])
        if not self.manual_result:
            result = self.evaluation_id.template_id._get_result(self.evaluation_id)
        else:
            result = self.result_id
        for evaluation in obj_evaluation.browse(evaluation_ids):
            evaluation.action_done(result=result, date_end=self.date_end)
