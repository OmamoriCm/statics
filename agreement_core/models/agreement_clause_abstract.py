# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AgreementClauseAbstract(models.AbstractModel):
    _name = "agreement.clause_abstract"
    _description = "Abstract Model for Agreement Clause"
    _order = "sequence, id"

    @api.multi
    @api.depends(
        "raw_content",
    )
    def _compute_content(self):
        MailTemplate = self.env["email.template"]
        for clause in self:
            # lang = clause.section_id.agreement_id.lang or "en_US"
            lang = "en_US"
            result = "-"
            if type(clause.id) is int:
                result = MailTemplate.with_context(lang=lang).render_template(
                    clause.raw_content, str(clause._model), clause.id
                )
            clause.content = result

    section_id = fields.Many2one(
        string="Section",
        comodel_name="agreement.section_abstract",
        required=True,
        select=True,
        ondelete="cascade",
    )
    name = fields.Char(
        string="Clause",
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
