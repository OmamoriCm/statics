# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AgreementAbstract(models.AbstractModel):
    _name = "agreement.abstract"
    _description = "Abstract Model for Agreement"

    @api.multi
    @api.depends(
        "raw_description",
    )
    def _compute_description(self):
        MailTemplate = self.env["email.template"]
        for agreement in self:
            # lang = agreement.lang or "en_US"
            lang = "en_US"
            description = "-"
            if type(agreement.id) is int:
                description = MailTemplate.with_context(lang=lang).render_template(
                    agreement.raw_description, str(agreement._model), agreement.id
                )
            agreement.description = description

    title = fields.Char(
        string="Title",
        required=True,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="agreement.type",
        required=True,
        select=True,
    )
    raw_description = fields.Text(
        string="Raw Description",
    )
    description = fields.Text(
        string="Description",
        compute="_compute_description",
        store=False,
    )
    note = fields.Text(
        string="Note",
    )
    section_ids = fields.One2many(
        string="Sections",
        comodel_name="agreement.section_abstract",
        inverse_name="agreement_id",
    )
    party_ids = fields.One2many(
        strig="Parties",
        comodel_name="agreement.party_abstract",
        inverse_name="agreement_id",
    )
    recital_ids = fields.One2many(
        string="Recitals",
        comodel_name="agreement.recital_abstract",
        inverse_name="agreement_id",
    )
    report_id = fields.Many2one(
        string="Report Template",
        comodel_name="ir.actions.report.xml",
        domain=[
            ("model", "=", "agreement.agreement"),
        ],
    )
