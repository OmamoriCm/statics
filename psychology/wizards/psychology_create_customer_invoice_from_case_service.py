# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class PsychologyCreateCustomerInvoiceFromCaseService(models.TransientModel):
    _name = "psychology.create_customer_invoice_from_case_service"
    _description = "Create Customer Invoice From Case Service"

    @api.model
    def _default_case_id(self):
        return self.env.context.get("active_id", False)

    date_invoice = fields.Date(
        string="Date Invoice",
    )
    case_id = fields.Many2one(
        string="# Case",
        comodel_name="psychology.case",
        required=True,
        default=lambda self: self._default_case_id(),
    )
    service_ids = fields.Many2many(
        string="Services",
        comodel_name="psychology.case_service",
        relation="rel_wizard_create_invoice_2_service",
        column1="wizard_id",
        column2="service_id",
    )

    @api.multi
    def action_create_invoice(self):
        self.ensure_one()
        self.case_id._create_customer_invoice(self.service_ids, self.date_invoice)
