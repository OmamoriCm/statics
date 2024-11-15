# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ServiceContractFixItemPaymentTerm(models.Model):
    _name = "service.contract_fix_item_payment_term"
    _description = "Service Contract Fix Item Payment Term"
    _order = "sequence, id"

    @api.depends(
        "detail_ids",
        "detail_ids.price_unit",
        "detail_ids.quantity",
        "detail_ids.uom_id",
        "detail_ids.tax_ids",
    )
    @api.multi
    def _compute_total(self):
        for record in self:
            amount_untaxed = amount_tax = amount_total = 0.0
            for detail in record.detail_ids:
                amount_untaxed += detail.amount_untaxed
                amount_tax += detail.amount_tax
                amount_total += detail.amount_total
            record.amount_untaxed = amount_untaxed
            record.amount_tax = amount_tax
            record.amount_total = amount_total

    @api.depends(
        "invoice_id",
        "contract_id.state",
    )
    def _compute_state(self):
        for record in self:
            if record.contract_id.state in ["draft", "confirm", "approve"]:
                state = "draft"
            elif record.contract_id.state in ["open", "done", "terminate"]:
                if record.invoice_id:
                    state = "invoiced"
                else:
                    state = "uninvoiced"
            else:
                state = "cancelled"
            record.state = state

    contract_id = fields.Many2one(
        string="# Contract",
        comodel_name="service.contract",
        ondelete="cascade",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="contract_id.currency_id",
        store=False,
    )
    date = fields.Date(
        string="Contract Date",
        related="contract_id.date",
        store=False,
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        related="contract_id.pricelist_id",
        store=False,
    )
    name = fields.Char(
        string="Term",
        required=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    fix_item_allowed_product_ids = fields.Many2many(
        string="Fix Item Allowed Products",
        comodel_name="product.product",
        related="contract_id.fix_item_allowed_product_ids",
        store=False,
    )
    fix_item_allowed_product_categ_ids = fields.Many2many(
        string="Fix Item Allowed Product Categories",
        comodel_name="product.category",
        related="contract_id.fix_item_allowed_product_categ_ids",
        store=False,
    )
    term_status = fields.Selection(
        string="Term Status",
        selection=[
            ("initial", "Initial"),
            ("addendum", "Adendum"),
        ],
        required=True,
        default="initial",
    )
    detail_ids = fields.One2many(
        string="Detail",
        comodel_name="service.contract_fix_item_payment_term_detail",
        inverse_name="payment_term_id",
        copy=True,
    )
    amount_untaxed = fields.Float(
        string="Untaxed",
        required=False,
        compute="_compute_total",
        store=True,
    )
    amount_tax = fields.Float(
        string="Tax",
        required=False,
        compute="_compute_total",
        store=True,
    )
    amount_total = fields.Float(
        string="Total",
        required=False,
        compute="_compute_total",
        store=True,
    )
    invoice_id = fields.Many2one(
        string="# Invoice",
        comodel_name="account.invoice",
        readonly=True,
        ondelete="restrict",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("uninvoiced", "Uninvoiced"),
            ("invoiced", "Invoiced"),
            ("cancelled", "Cancelled"),
        ],
        compute="_compute_state",
        store=True,
    )

    @api.multi
    def action_create_invoice(self):
        for record in self:
            record._create_invoice()

    @api.multi
    def action_delete_invoice(self):
        for record in self:
            record._delete_invoice()

    @api.multi
    def action_disconnect_invoice(self):
        for record in self:
            record._disconnect_invoice()

    @api.multi
    def _create_invoice(self):
        self.ensure_one()
        invoice = self.env["account.invoice"].create(self._prepare_invoice_data())
        self.write(
            {
                "invoice_id": invoice.id,
            }
        )
        for detail in self.detail_ids:
            detail._create_invoice_line()
        invoice.button_reset_taxes()

    @api.multi
    def _disconnect_invoice(self):
        self.ensure_one()
        self.write(
            {
                "invoice_id": False,
            }
        )

    @api.multi
    def _get_fix_item_receivable_journal(self):
        self.ensure_one()
        contract = self.contract_id
        return contract.fix_item_receivable_journal_id

    @api.multi
    def _get_fix_item_receivable_account(self):
        self.ensure_one()
        contract = self.contract_id
        return contract.fix_item_receivable_account_id

    @api.multi
    def _prepare_invoice_data(self):
        self.ensure_one()
        contract = self.contract_id
        partner = contract.partner_invoice_id or contract.partner_id
        journal = self._get_fix_item_receivable_journal()
        account = self._get_fix_item_receivable_account()
        return {
            "partner_id": partner.id,
            "date_invoice": False,  # TODO
            "journal_id": journal.id,
            "account_id": account.id,
            "currency_id": contract.currency_id.id,
            "origin": contract.name,
            "name": contract.title,
        }

    @api.multi
    def _delete_invoice(self):
        self.ensure_one()
        invoice = self.invoice_id
        self.detail_ids.write({"invoice_line_id": False})
        self.write(
            {
                "invoice_id": False,
            }
        )
        invoice.unlink()
