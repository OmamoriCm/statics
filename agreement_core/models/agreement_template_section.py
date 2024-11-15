# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AgreementTemplateSection(models.Model):
    _name = "agreement.template_section"
    _inherit = "agreement.section_abstract"
    _description = "Agreement Template Section"

    agreement_id = fields.Many2one(
        comodel_name="agreement.template",
    )
    clause_ids = fields.One2many(
        comodel_name="agreement.template_clause",
        inverse_name="section_id",
    )

    @api.multi
    def _prepare_clause(self):
        self.ensure_one()
        result = []
        for clause in self.clause_ids:
            result.append(
                (
                    0,
                    0,
                    {
                        "name": clause.name,
                        "title": clause.title,
                        "sequence": clause.sequence,
                        "raw_content": clause.raw_content,
                    },
                )
            )
        return result
