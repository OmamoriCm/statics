# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class PsychologyFinishService(models.TransientModel):
    _name = "psychology.finish_service"
    _description = "Finish Case Service"

    @api.model
    def _default_service_ids(self):
        active_ids = self.env.context.get("active_ids", [])
        obj_service = self.env["psychology.case_service"]
        criteria = [
            ("id", "in", active_ids),
            ("state", "in", ["draft", "open"]),
        ]
        service_ids = obj_service.search(criteria).ids
        return [(6, 0, service_ids)]

    date_done = fields.Date(
        string="Date Finish",
        required=True,
    )
    service_ids = fields.Many2many(
        string="Services",
        comodel_name="psychology.case_service",
        relation="rel_wizard_finish_service",
        column1="wizard_id",
        column2="service_id",
        default=lambda self: self._default_service_ids(),
        readonly=True,
    )

    @api.multi
    def action_finish_service(self):
        self.ensure_one()
        self.service_ids.action_done(self.date_done)
