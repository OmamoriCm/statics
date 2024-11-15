# -*- coding: utf-8 -*-
# Copyright 2018-2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AgreementPartyAbstract(models.AbstractModel):
    _name = "agreement.party_abstract"
    _description = "Abstract Model for Agreement Party"
    _order = "sequence, id"

    @api.multi
    @api.depends(
        "party_id",
    )
    def _compute_allowed_contact_ids(self):
        obj_partner = self.env["res.partner"]
        for party in self:
            result = []
            if (
                party.party_id
                and party.party_id.is_company
                and not party.party_id.parent_id
            ):
                criteria = [
                    ("id", "child_of", party.party_id.id),
                    ("is_company", "=", False),
                ]
                result = obj_partner.search(criteria).ids
            elif (
                party.party_id
                and not party.party_id.is_company
                and not party.party_id.parent_id
            ):
                result = [party.party_id.id]
            party.allowed_contact_ids = result

    agreement_id = fields.Many2one(
        string="Agreement",
        comodel_name="agreement.abstract",
        required=True,
        select=True,
        ondelete="cascade",
    )
    name = fields.Char(
        string="Party Alias",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        required=True,
    )
    party_id = fields.Many2one(
        string="Party",
        comodel_name="res.partner",
        domain=[
            ("parent_id", "=", False),
        ],
    )
    allowed_contact_ids = fields.Many2many(
        string="Allowed Contacts",
        comodel_name="res.partner",
        compute="_compute_allowed_contact_ids",
        store=False,
    )
    contact_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
    )

    @api.onchange(
        "party_id",
    )
    def onchange_contact_id(self):
        self.contact_id = False
