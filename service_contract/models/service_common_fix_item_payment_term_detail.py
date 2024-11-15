# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ServiceCommonFixItemPaymentTermDetail(models.AbstractModel):
    _name = "service.common_fix_item_payment_term_detail"
    _description = "Service Common Fix Item Payment Term Detail"

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
        comodel_name="service.common_fix_item_payment_term",
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
