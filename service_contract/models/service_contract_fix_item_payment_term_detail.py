# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ServiceContractFixItemPaymentTermDetail(models.Model):
    _name = "service.contract_fix_item_payment_term_detail"
    _description = "Service Contract Fix Item Payment Term Detail"

    @api.depends(
        "price_unit",
        "quantity",
        "tax_ids",
    )
    @api.multi
    def _compute_total(self):
        for record in self:
            amount_untaxed = amount_tax = amount_total = 0.0
            tax_comp = record.tax_ids.compute_all(
                price_unit=record.price_unit,
                quantity=record.quantity,
                product=record.product_id,
            )
            amount_untaxed += tax_comp["total"]
            amount_tax += tax_comp["total_included"] - tax_comp["total"]
            amount_total += tax_comp["total_included"]
            record.amount_untaxed = amount_untaxed
            record.amount_tax = amount_tax
            record.amount_total = amount_total

    @api.depends(
        "product_id",
    )
    @api.multi
    def _compute_uom(self):
        for record in self:
            categ_id = False
            if record.product_id:
                categ_id = record.product_id.uom_id.category_id
            record.allowed_uom_categ_id = categ_id

    payment_term_id = fields.Many2one(
        string="Payment Term",
        comodel_name="service.contract_fix_item_payment_term",
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    name = fields.Char(
        string="Description",
        required=True,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
    )
    price_unit = fields.Float(
        string="Price Unit",
        required=True,
        default=1.0,
    )
    quantity = fields.Float(
        string="Qty",
        required=True,
        default=1.0,
    )
    allowed_uom_categ_id = fields.Many2one(
        string="Allowed UoM Categ",
        comodel_name="product.uom.categ",
        compute="_compute_uom",
        store=False,
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
        required=True,
    )
    tax_ids = fields.Many2many(
        string="Taxes",
        comodel_name="account.tax",
        relation="rel_contract_fix_item_payment_term_detail_2_tax",
        column1="fix_item_id",
        column2="tax_id",
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
    invoice_line_id = fields.Many2one(
        string="Invoice Line",
        comodel_name="account.invoice.line",
        readonly=True,
        ondelete="restrict",
    )
    pricelist_id = fields.Many2one(
        string="Price List",
        comodel_name="product.pricelist",
        required=False,
    )

    @api.depends(
        "payment_term_id",
    )
    def _compute_date(self):
        for document in self:
            document.date = document.payment_term_id.contract_id.date

    date = fields.Date(
        string="Date",
        compute="_compute_date",
        store=False,
    )

    @api.depends(
        "payment_term_id",
    )
    def _compute_currency(self):
        for document in self:
            document.currency_id = document.payment_term_id.contract_id.currency_id

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        compute="_compute_currency",
        required=False,
    )

    @api.onchange(
        "product_id",
    )
    def onchange_uom_id(self):
        self.uom_id = False
        if self.product_id:
            self.uom_id = self.product_id.uom_id

    @api.onchange(
        "product_id",
    )
    def onchange_tax_ids(self):
        self.tax_ids = []
        if self.product_id:
            self.tax_ids = self.product_id.taxes_id

    @api.onchange(
        "product_id",
    )
    def onchange_name(self):
        self.name = ""
        if self.product_id:
            self.name = self.product_id.display_name

    @api.multi
    def _create_invoice_line(self):
        self.ensure_one()
        line = self.env["account.invoice.line"].create(self._prepare_invoice_line())
        self.write(
            {
                "invoice_line_id": line.id,
            }
        )

    @api.multi
    def _prepare_invoice_line(self):
        self.ensure_one()
        payment_term = self.payment_term_id
        contract = payment_term.contract_id
        aa = contract.analytic_account_id
        return {
            "invoice_id": payment_term.invoice_id.id,
            "product_id": self.product_id.id,
            "name": self.name,
            "account_id": self.product_id.property_account_income.id,
            "quantity": self.quantity,
            "uos_id": self.uom_id.id,
            "price_unit": self.price_unit,
            "invoice_line_tax_id": [(6, 0, self.tax_ids.ids)],
            "account_analytic_id": aa and aa.id or False,
        }

    @api.onchange(
        "pricelist_id",
        "product_id",
        "quantity",
        "date",
        "uom_id",
    )
    def onchange_price_unit(self):
        price_unit = 0.0
        obj_uom = self.env["product.uom"]
        qty = 0.0

        ctx = {}
        if self.date:
            ctx.update({"date": self.date})

        if self.uom_id:
            qty = obj_uom._compute_qty_obj(
                from_unit=self.uom_id,
                qty=self.quantity,
                to_unit=self.product_id.uom_id,
            )

        if self.product_id and self.pricelist_id:
            price_unit = self.pricelist_id.with_context(ctx).price_get(
                prod_id=self.product_id.id,
                qty=qty,
            )[self.pricelist_id.id]

        if self.uom_id:
            price_unit = obj_uom._compute_price(
                from_uom_id=self.product_id.uom_id.id,
                price=price_unit,
                to_uom_id=self.uom_id.id,
            )

        self.price_unit = price_unit
