# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AgreementTemplate(models.Model):
    _name = "agreement.template"
    _description = "Agreement Template"
    _inherit = [
        "agreement.abstract",
    ]
    _rec_name = "title"

    active = fields.Boolean(
        string="Active",
        default=True,
    )
    section_ids = fields.One2many(
        comodel_name="agreement.template_section",
        inverse_name="agreement_id",
    )
    party_ids = fields.One2many(
        comodel_name="agreement.template_party",
        inverse_name="agreement_id",
    )
    recital_ids = fields.One2many(
        comodel_name="agreement.template_recital",
        inverse_name="agreement_id",
    )
    appendix_ids = fields.One2many(
        comodel_name="agreement.template_appendix",
        inverse_name="agreement_id",
    )

    @api.multi
    def _prepare_recital(self):
        self.ensure_one()
        result = []
        for recital in self.recital_ids:
            result.append(
                (
                    0,
                    0,
                    {
                        "name": recital.name,
                        "title": recital.title,
                        "sequence": recital.sequence,
                        "raw_content": recital.raw_content,
                    },
                )
            )
        return result

    @api.multi
    def _prepare_section(self):
        self.ensure_one()
        result = []
        for section in self.section_ids:
            result.append(
                (
                    0,
                    0,
                    {
                        "name": section.name,
                        "title": section.title,
                        "sequence": section.sequence,
                        "raw_content": section.raw_content,
                        "clause_ids": section._prepare_clause(),
                    },
                )
            )
        return result

    @api.multi
    def _prepare_appendix(self):
        self.ensure_one()
        result = []
        for appendix in self.appendix_ids:
            result.append(
                (
                    0,
                    0,
                    {
                        "name": appendix.name,
                        "title": appendix.title,
                        "sequence": appendix.sequence,
                        "raw_content": appendix.raw_content,
                    },
                )
            )
        return result

    @api.multi
    def _prepare_party(self):
        self.ensure_one()
        result = []
        for party in self.party_ids:
            partner_id = party.party_id and party.party_id.id or False
            contact_id = party.contact_id and party.contact_id.id or False
            result.append(
                (
                    0,
                    0,
                    {
                        "name": party.name,
                        "sequence": party.sequence,
                        "party_id": partner_id,
                        "contact_id": contact_id,
                    },
                )
            )
        return result
