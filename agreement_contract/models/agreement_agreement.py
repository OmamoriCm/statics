# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AgreementAgreement(models.Model):
    _name = "agreement.agreement"
    _inherit = [
        "agreement.agreement",
    ]

    analytic_id = fields.Many2one(
        string="Contract",
        comodel_name="account.analytic.account",
        domain=[
            ("type", "=", "contract"),
        ],
    )
