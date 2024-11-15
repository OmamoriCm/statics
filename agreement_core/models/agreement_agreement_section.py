# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AgreementAgreementSection(models.Model):
    _name = "agreement.agreement_section"
    _inherit = "agreement.section_abstract"
    _description = "Agreement Section"

    agreement_id = fields.Many2one(
        comodel_name="agreement.agreement",
    )
    clause_ids = fields.One2many(
        comodel_name="agreement.agreement_clause",
        inverse_name="section_id",
    )
