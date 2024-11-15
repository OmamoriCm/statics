# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class PsychologyCreateSupplierInvoiceFromCaseActivity(models.TransientModel):
    _name = "psychology.create_supplier_invoice_from_case_activity"
    _description = "Create Supplier Invoice From Case Activity"

    @api.model
    def _default_currency_id(self):
        return self.env.user.company_id.currency_id.id

    date_invoice = fields.Date(
        string="Date Invoice",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
        default=lambda self: self._default_currency_id(),
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=True,
    )
    account_id = fields.Many2one(
        string="Payable Account",
        comodel_name="account.account",
        required=True,
    )
    activity_ids = fields.Many2many(
        string="Activities",
        comodel_name="psychology.case_activity",
        relation="rel_wizard_create_supplier_invoice_2_activity",
        column1="wizard_id",
        column2="activity_id",
    )

    @api.multi
    def action_create_invoice(self):
        self.ensure_one()
        self._create_supplier_invoice()

    @api.onchange(
        "currency_id",
    )
    def onchange_activity_ids(self):
        self.activity_ids = False
        if self.currency_id:
            obj_activity = self.env["psychology.case_activity"]
            active_ids = self.env.context.get("active_ids", [])
            criteria = [
                ("id", "in", active_ids),
                ("invoice_state", "=", "2binvoiced"),
                ("currency_id", "=", self.currency_id.id),
                ("state", "=", "done"),
            ]
            self.activity_ids = obj_activity.search(criteria).ids

    @api.onchange(
        "currency_id",
    )
    def onchange_account_id(self):
        self.account_id = False

    @api.onchange(
        "currency_id",
    )
    def onchange_journal_id(self):
        self.account_id = False

    @api.multi
    def _create_supplier_invoice(self):
        self.ensure_one()
        obj_invoice = self.env["account.invoice"]
        partners = self.activity_ids.mapped("responsible_id")
        for partner in partners:
            invoice = obj_invoice.create(
                self._prepare_supplier_invoice_data(partner=partner)
            )
            activities = self.activity_ids.filtered(
                lambda r: r.responsible_id.id == partner.id
            )
            for activity in activities:
                activity._create_supplier_invoice_line(invoice)

    @api.multi
    def _prepare_supplier_invoice_data(self, partner):
        self.ensure_one()
        return {
            "partner_id": partner.id,
            "date_invoice": self.date_invoice,
            "journal_id": self.journal_id.id,
            "account_id": self.account_id.id,
            "currency_id": self.currency_id.id,
            "type": "in_invoice",
        }
