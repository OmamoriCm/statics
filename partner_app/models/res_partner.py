# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def button_toggle_customer(self):
        for partner in self:
            partner._toggle_customer()

    @api.multi
    def button_toggle_supplier(self):
        for partner in self:
            partner._toggle_supplier()

    @api.multi
    def _toggle_customer(self):
        self.ensure_one()
        criteria = [
            "|",
            ("id", "=", self.id),
            ("commercial_partner_id", "=", self.id),
        ]
        self.env["res.partner"].search(criteria).write(
            {
                "customer": not self.customer,
            }
        )

    @api.multi
    def _toggle_supplier(self):
        self.ensure_one()
        criteria = [
            "|",
            ("id", "=", self.id),
            ("commercial_partner_id", "=", self.id),
        ]
        self.env["res.partner"].search(criteria).write(
            {
                "supplier": not self.supplier,
            }
        )
