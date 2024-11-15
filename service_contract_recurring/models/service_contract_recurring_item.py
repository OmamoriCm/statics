# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class ServiceContractRecurringItem(models.Model):
    _name = "service.contract_recurring_item"
    _description = "Service Contract Recurring Item"
    _order = "sequence, id"

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

    contract_id = fields.Many2one(
        string="# Contract",
        comodel_name="service.contract",
        ondelete="cascade",
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
    recurring_item_allowed_product_ids = fields.Many2many(
        string="Recurring Item Allowed Products",
        comodel_name="product.product",
        related="contract_id.recurring_item_allowed_product_ids",
        store=False,
    )
    recurring_item_allowed_product_categ_ids = fields.Many2many(
        string="Recurring Item Allowed Product Categories",
        comodel_name="product.category",
        related="contract_id.recurring_item_allowed_product_categ_ids",
        store=False,
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
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        related="contract_id.pricelist_id",
        store=False,
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
        relation="rel_contract_recurring_item_2_tax",
        column1="recurring_item_id",
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

    @api.multi
    def _create_invoice_line(self, invoice, period):
        self.ensure_one()
        self.env["account.invoice.line"].create(
            self._prepare_invoice_line(invoice, period)
        )

    @api.multi
    def _prepare_invoice_line(self, invoice, period):
        self.ensure_one()
        aa = period.analytic_account_id
        name = """{}

        Period: {} to {}
        """.format(
            self.product_id.name,
            period.date_start,
            period.date_end,
        )
        return {
            "invoice_id": invoice.id,
            "name": name,
            "product_id": self.product_id.id,
            "account_id": self.product_id.property_account_income.id,  # TODO
            "quantity": self.quantity,
            "uos_id": self.uom_id.id,
            "price_unit": self.price_unit,
            "invoice_line_tax_id": [(6, 0, self.tax_ids.ids)],
            "account_analytic_id": aa and aa.id or False,
        }

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

    @api.onchange(
        "product_id",
        "pricelist_id",
        "uom_id",
    )
    def onchange_price_unit(self):
        self.price_unit = 0.0
        if self.product_id and self.pricelist_id and self.uom_id:
            price_unit = self.pricelist_id.price_get(
                prod_id=self.product_id.id, qty=1.0
            )[self.pricelist_id.id]
            self.price_unit = price_unit

    @api.multi
    def _prepare_income_realization_debit_move_line(self, period):
        self.ensure_one()
        contract = self.contract_id
        account = self._get_income_realization_account()
        # TODO: Multi-currency support
        name = "Income realization {} - {} - period {} S.D. {}".format(
            contract.name,
            self.product_id.name,
            period.date_start,
            period.date_end,
        )
        return (
            0,
            0,
            {
                "name": name,
                "partner_id": contract.partner_id.id,
                "product_id": self.product_id.id,
                "account_id": account.id,
                "credit": self.amount_untaxed > 0.0 and abs(self.amount_untaxed) or 0.0,
                "debit": self.amount_untaxed < 0.0 and abs(self.amount_untaxed) or 0.0,
                "analytic_account_id": period.analytic_account_id.id,
            },
        )

    @api.multi
    def _get_income_realization_account(self):
        self.ensure_one()
        result = False
        product = self.product_id
        categ = product.categ_id
        if product.property_account_income:
            result = product.property_account_income

        if not result:
            result = categ.property_account_income_categ

        if not result:
            error_msg = _("No income account defined")
            raise UserError(error_msg)

        return result
