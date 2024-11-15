# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class PartnerStartEvaluation(models.TransientModel):
    _name = "partner.start_evaluation"
    _description = "Start Partner Evaluation"

    @api.model
    def _default_date_start(self):
        return fields.Datetime.now()

    date_start = fields.Datetime(
        string="Date Start",
        required=True,
        default=lambda self: self._default_date_start(),
    )

    @api.multi
    def action_start(self):
        self.ensure_one()
        obj_evaluation = self.env["partner.evaluation"]
        evaluation_ids = self._context.get("active_ids", [])
        for evaluation in obj_evaluation.browse(evaluation_ids):
            evaluation.action_start(date_start=self.date_start)
