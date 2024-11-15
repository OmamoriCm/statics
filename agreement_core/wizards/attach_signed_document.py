# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AgreementAttachSignedDocument(models.TransientModel):
    _name = "agreement.attach_signed_document"
    _description = "Attach Signed Document"

    @api.model
    def _default_agreement_id(self):
        return self._context.get("active_id", False)

    document = fields.Binary(
        string="Signed Document",
        required=True,
    )
    agreement_id = fields.Many2one(
        string="Agreement",
        comodel_name="agreement.agreement",
        required=True,
        default=lambda self: self._default_agreement_id(),
    )

    @api.multi
    def action_confirm(self):
        for wiz in self:
            wiz._attach_document()

    @api.multi
    def _attach_document(self):
        self.ensure_one()
        agreement_id = self.env.context.get("active_id", [])
        agreement = self.env["agreement.agreement"].browse([agreement_id])[0]
        obj_attachment = self.env["ir.attachment"]
        attachment = obj_attachment.create(self._prepare_attachment())
        agreement.write(
            {
                "signed_document_id": attachment.id,
            }
        )

    @api.multi
    def _prepare_attachment(self):
        self.ensure_one()
        agreement = self.agreement_id
        return {
            "name": agreement.name,
            "company_id": agreement.company_id.id,
            "res_model": "agreement.agreement",
            "res_id": agreement.id,
            "type": "binary",
            "datas": self.document,
        }
