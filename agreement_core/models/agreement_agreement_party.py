# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AgreementAgreementParty(models.Model):
    _name = "agreement.agreement_party"
    _description = "Agreement Party"
    _inherit = "agreement.party_abstract"

    agreement_id = fields.Many2one(
        comodel_name="agreement.agreement",
    )
