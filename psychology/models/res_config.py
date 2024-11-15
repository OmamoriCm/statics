# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ResConfig(models.TransientModel):
    _name = "psychology.config_setting"
    _inherit = "res.config.settings"

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
    )
    module_psychology_assesment = fields.Boolean(
        string="Assesment",
    )
    module_psychology_appointment = fields.Boolean(
        string="Appointment",
    )
    module_psychology_intervention = fields.Boolean(
        string="Invertention",
    )
