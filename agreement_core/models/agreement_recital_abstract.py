# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AgreementRecitalAbstract(models.AbstractModel):
    _name = "agreement.recital_abstract"
    _description = "Abstract Model for Agreement Recital"
    _order = "sequence, id"

    @api.multi
    @api.depends(
        "raw_content",
    )
    def _compute_content(self):
        MailTemplate = self.env["email.template"]
        for recital in self:
            # lang = recital.agreement_id.lang or "en_US"
            lang = "en_US"
            result = "-"
            if type(recital.id) is int:
                result = MailTemplate.with_context(lang=lang).render_template(
                    recital.raw_content, str(recital._model), recital.id
                )
            recital.content = result

    agreement_id = fields.Many2one(
        string="Agreement",
        comodel_name="agreement.abstract",
        required=True,
        select=True,
        ondelete="cascade",
    )
    name = fields.Char(
        string="Recital",
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
