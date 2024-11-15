# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class PsychologyFinishActivity(models.TransientModel):
    _name = "psychology.finish_activity"
    _description = "Finish Cas Activity"

    @api.model
    def _default_activity_ids(self):
        active_ids = self.env.context.get("active_ids", [])
        obj_activity = self.env["psychology.case_activity"]
        criteria = [
            ("id", "in", active_ids),
            ("state", "in", ["draft", "open"]),
        ]
        activity_ids = obj_activity.search(criteria).ids
        return [(6, 0, activity_ids)]

    date_done = fields.Date(
        string="Date Finish",
        required=True,
    )
    activity_ids = fields.Many2many(
        string="Activities",
        comodel_name="psychology.case_activity",
        relation="rel_wizard_finish_activity",
        column1="wizard_id",
        column2="activity_id",
        default=lambda self: self._default_activity_ids(),
        readonly=True,
    )

    @api.multi
    def action_finish_activity(self):
        self.ensure_one()
        self.activity_ids.action_done(self.date_done)
