# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AgreementAgreementRecital(models.Model):
    _name = "agreement.agreement_recital"
    _inherit = "agreement.recital_abstract"
    _description = "Agreement Recital"

    agreement_id = fields.Many2one(
        comodel_name="agreement.agreement",
    )
