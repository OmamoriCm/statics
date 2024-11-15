# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AgreementSectionAbstract(models.AbstractModel):
    _name = "agreement.section_abstract"
    _description = "Abstract Model for Agreement Section"
    _order = "sequence, id"

    @api.multi
    @api.depends(
        "raw_content",
    )
    def _compute_content(self):
        MailTemplate = self.env["email.template"]
        for section in self:
            # lang = section.agreement_id.lang or "en_US"
            lang = "en_US"
            result = "-"
            if type(section.id) is int:
                result = MailTemplate.with_context(lang=lang).render_template(
                    section.raw_content, str(section._model), section.id
                )
            section.content = result

    agreement_id = fields.Many2one(
        string="Agreement",
        comodel_name="agreement.abstract",
        required=True,
        select=True,
        ondelete="cascade",
    )
    name = fields.Char(
        string="Section",
        required=True,
    )
    title = fields.Char(
        string="Title",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        required=True,
    )
    raw_content = fields.Text(
        string="Raw Content",
    )
    content = fields.Text(
        string="Content",
        compute="_compute_content",
        store=False,
    )
    clause_ids = fields.One2many(
        string="Clauses",
        comodel_name="agreement.clause_abstract",
        inverse_name="section_id",
    )
