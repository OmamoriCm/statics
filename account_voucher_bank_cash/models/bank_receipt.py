# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class BankReceipt(models.Model):
    _name = "account.bank_receipt"
    _inherit = "account.bank_voucher"
    _description = "Bank Receipt"

    @api.model
    def _default_type_id(self):
        return self.env.ref("account_voucher_bank_cash.voucher_type_bank_receipt").id

    type_id = fields.Many2one(
        default=lambda self: self._default_type_id(),
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
        related="company_id.currency_id",
        store=True,
    )

    line_ids = fields.One2many(
        comodel_name="account.bank_receipt_line",
    )
    line_dr_ids = fields.One2many(
        comodel_name="account.bank_receipt_line",
    )
    line_cr_ids = fields.One2many(
        comodel_name="account.bank_receipt_line",
    )


class BankReceiptLine(models.Model):
    _name = "account.bank_receipt_line"
    _inherit = "account.voucher_line_common"
    _description = "Bank Receipt Line"

    voucher_id = fields.Many2one(
        comodel_name="account.bank_receipt",
    )
    tax_ids = fields.One2many(
        comodel_name="account.bank_receipt_line_tax",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="voucher_id.currency_id",
        store=True,
    )
    company_currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="voucher_id.company_currency_id",
        store=True,
    )


class BankReceiptLineTax(models.Model):
    _name = "account.bank_receipt_line_tax"
    _inherit = "account.voucher_line_tax_common"
    _description = "Bank Receipt Line Tax"

    voucher_line_id = fields.Many2one(
        comodel_name="account.bank_receipt_line",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="voucher_line_id.currency_id",
        store=True,
    )
    company_currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="voucher_line_id.company_currency_id",
        store=True,
    )
