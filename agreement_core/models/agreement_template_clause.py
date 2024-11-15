# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AgreementTemplateClause(models.Model):
    _name = "agreement.template_clause"
    _description = "Agreement Template Clause"
    _inherit = "agreement.clause_abstract"

    section_id = fields.Many2one(
        comodel_name="agreement.template_section",
    )
