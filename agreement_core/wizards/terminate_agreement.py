# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AgreementTerminateAgreement(models.TransientModel):
    _name = "agreement.terminate_agreement"
    _description = "Terminate Agreement"

    terminate_reason_id = fields.Many2one(
        string="Terminate Reason",
        comodel_name="agreement.termination_reason",
        required=True,
    )

    @api.multi
    def action_confirm(self):
        for wiz in self:
            wiz._confirm_terminate()

    @api.multi
    def _confirm_terminate(self):
        self.ensure_one()
        agreement_ids = self.env.context.get("active_ids", [])
        agreements = self.env["agreement.agreement"].browse(agreement_ids)
        agreements.button_terminate(self.terminate_reason_id.id)
