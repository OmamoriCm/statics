# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class PsychologyCaseService(models.Model):
    _name = "psychology.case_service"
    _inherit = [
        "mail.thread",
        "base.sequence_document",
        "base.workflow_policy_object",
    ]
    _description = "Psychology Case Service"

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

    @api.multi
    def _compute_reference_id(self):
        for record in self:
            if record.model and record.res_id:
                record.reference_id = "{},{}".format(record.model, record.res_id)

    case_id = fields.Many2one(
        string="# Case",
        comodel_name="psychology.case",
        ondelete="cascade",
        required=True,
    )
    partner_id = fields.Many2one(
        string="Client",
        comodel_name="res.partner",
        readonly=True,
        related="case_id.partner_id",
        store=True,
    )
    name = fields.Char(
        string="# Document",
        required=True,
        default="/",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    model = fields.Char(
        string="Related Document Model",
        index=True,
    )
    reference_id = fields.Reference(
        string="Reference",
        compute="_compute_reference_id",
        store=False,
        selection=[
            ("account.invoice", "Invoice"),
        ],
    )
    res_id = fields.Integer(
        string="Related Document ID",
        index=True,
    )
    service_allowed_product_ids = fields.Many2many(
        string="Service Allowed Products",
        comodel_name="product.product",
        related="case_id.type_id.service_allowed_product_ids",
        store=False,
    )
    service_allowed_product_categ_ids = fields.Many2many(
        string="Fix Item Allowed Product Categories",
        comodel_name="product.category",
        related="case_id.type_id.service_allowed_product_categ_ids",
        store=False,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="pricelist_id.currency_id",
        store=True,
    )
    price_unit = fields.Float(
        string="Price Unit",
        required=True,
        default=1.0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    quantity = fields.Float(
        string="Qty",
        required=True,
        default=1.0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
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
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    tax_ids = fields.Many2many(
        string="Taxes",
        comodel_name="account.tax",
        relation="rel_psychology_case_service_2_tax",
        column1="fix_item_id",
        column2="tax_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
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
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    invoice_line_id = fields.Many2one(
        string="Invoice Line",
        comodel_name="account.invoice.line",
        readonly=True,
        ondelete="restrict",
    )
    invoice_id = fields.Many2one(
        string="# Invoice",
        comodel_name="account.invoice",
        related="invoice_line_id.invoice_id",
        store=True,
        readonly=True,
    )
    date_done = fields.Date(
        string="Date Finish",
        readonly=True,
    )
    note = fields.Text(
        string="Note",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "To Do"),
            ("open", "Doing"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        required=True,
        readonly=True,
        default="draft",
    )
    invoice_state = fields.Selection(
        string="Invoice State",
        selection=[
            ("uninvoiceable", "Uninvoiceable"),
            ("2binvoiced", "To Be Invoiced"),
            ("invoiced", "Invoiced"),
        ],
        required=True,
        readonly=True,
        default="2binvoiced",
    )
    # Policy Field
    start_ok = fields.Boolean(
        string="Can Start",
        compute="_compute_policy",
    )
    finish_ok = fields.Boolean(
        string="Can Finish",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )
    unlink_invoice_ok = fields.Boolean(
        string="Can Delete Customer Invoice",
        compute="_compute_policy",
    )

    @api.multi
    def action_start(self):
        for record in self:
            record.write(record._prepare_start_data())

    @api.multi
    def action_done(self, date_done=False):
        for record in self:
            record.write(record._prepare_done_data(date_done))

    @api.multi
    def action_cancel(self):
        for record in self:
            record.write(record._prepare_cancel_data())

    @api.multi
    def action_restart(self):
        for record in self:
            record.write(record._prepare_restart_data())

    @api.multi
    def action_unlink_invoice(self):
        for record in self:
            record._unlink_customer_invoice()

    @api.multi
    def _prepare_start_data(self):
        self.ensure_one()
        return {
            "state": "open",
        }

    @api.multi
    def _prepare_done_data(self, date_done):
        self.ensure_one()
        date_done = date_done or fields.Date.today()
        return {
            "state": "done",
            "date_done": date_done,
        }

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
            "date_done": False,
        }

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
        }

    @api.model
    def referencable_models(self):
        obj = self.env("res.request.link")
        res = obj.search([])
        return [(r.object, r.name) for r in res]

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
    def _create_customer_invoice_line(self, invoice):
        self.ensure_one()
        obj_line = self.env["account.invoice.line"]
        line = obj_line.create(self._prepare_invoice_line(invoice))
        self.write(
            {
                "invoice_state": "invoiced",
                "invoice_line_id": line.id,
            }
        )

    @api.multi
    def _get_invoice_line_name(self):
        self.ensure_one()
        name = """{}
        # Case: {}
        """.format(
            self.product_id.name,
            self.case_id.name,
        )
        return name

    @api.multi
    def _prepare_invoice_line(self, invoice):
        self.ensure_one()
        aa = self.analytic_account_id
        return {
            "invoice_id": invoice.id,
            "name": self._get_invoice_line_name(),
            "product_id": self.product_id.id,
            "account_id": self.product_id.property_account_income.id,
            "quantity": self.quantity,
            "uos_id": self.uom_id.id,
            "price_unit": self.price_unit,
            "invoice_line_tax_id": [(6, 0, self.tax_ids.ids)],
            "account_analytic_id": aa and aa.id or False,
        }

    @api.multi
    def _unlink_customer_invoice(self):
        self.ensure_one()
        invoices = self.case_id.customer_invoice_ids - self.invoice_id
        self.case_id.write({"customer_invoice_ids": [(6, 0, invoices.ids)]})
        self.case_id._unlink_customer_invoice(self.invoice_id)

    @api.model
    def create(self, values):
        _super = super(PsychologyCaseService, self)
        result = _super.create(values)
        sequence = result._create_sequence()
        result.write(
            {
                "name": sequence,
            }
        )
        return result

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for record in self:
            if record.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(PsychologyCaseService, self)
        _super.unlink()
