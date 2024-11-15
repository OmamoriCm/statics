# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ServiceContractManHour(models.Model):
    _name = "service.contract_man_hour"
    _inherit = [
        "mail.thread",
    ]
    _description = "Service Contract Man Hour"
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

    @api.depends(
        "invoice_id",
    )
    @api.multi
    def _compute_invoice_state(self):
        for document in self:
            document.invoice_state = "tobeinvoiced"
            if document.invoice_id:
                document.invoice_state = "invoiced"

    @api.depends(
        "analytic_account_id",
    )
    @api.multi
    def _compute_timesheet_ids(self):
        obj_timesheet = self.env["hr.analytic.timesheet"]
        for document in self:
            result = []
            if document.analytic_account_id:
                criteria = [("account_id", "=", document.analytic_account_id.id)]
                timesheets = obj_timesheet.search(criteria)
                result = timesheets.ids
            document.timesheet_ids = result

    @api.depends(
        "quantity",
        "uom_id",
        "timesheet_ids",
        "timesheet_ids.unit_amount",
        "timesheet_ids.account_id",
    )
    def _compute_man_hour(self):
        obj_uom = self.env["product.uom"]
        for document in self:
            prepaid_usage = prepaid_total = prepaid_diff = 0.0
            uom = False
            if document.quantity and document.uom_id:
                criteria = [
                    ("category_id", "=", document.uom_id.category_id.id),
                    ("uom_type", "=", "reference"),
                ]
                uoms = obj_uom.search(criteria)
                if len(uoms) > 0:
                    uom = uoms[0]
                if uom:
                    prepaid_total = obj_uom._compute_qty_obj(
                        from_unit=document.uom_id,
                        qty=document.quantity,
                        to_unit=uom,
                    )
            for timesheet in document.timesheet_ids:
                prepaid_usage += timesheet.unit_amount
            prepaid_diff = prepaid_total - prepaid_usage
            document.prepaid_usage = prepaid_usage
            document.prepaid_total = prepaid_total
            document.prepaid_diff = prepaid_diff

    contract_id = fields.Many2one(
        string="# Contract",
        comodel_name="service.contract",
        ondelete="cascade",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        related="contract_id.partner_id",
        store=True,
        readonly=True,
    )
    responsible_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        related="contract_id.responsible_id",
        store=True,
        readonly=True,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="service.contract_type",
        related="contract_id.type_id",
        store=True,
        readonly=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    man_hour_allowed_product_ids = fields.Many2many(
        string="Man Hour Allowed Products",
        comodel_name="product.product",
        related="contract_id.type_id.man_hour_allowed_product_ids",
        store=False,
    )
    man_hour_allowed_product_categ_ids = fields.Many2many(
        string="Man Hour Allowed Product Categories",
        comodel_name="product.category",
        related="contract_id.type_id.man_hour_allowed_product_categ_ids",
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
        relation="rel_contract_man_hour_2_tax",
        column1="man_hour_id",
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
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        ondelete="restrict",
        readonly=True,
    )
    invoice_method = fields.Selection(
        string="Invoice Method",
        selection=[
            ("prepaid", "Prepaid"),
            ("postpaid", "Post Paid"),
        ],
        default="prepaid",
        required=True,
    )
    contract_state = fields.Selection(
        string="Contract State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("approve", "Ready to Start"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("terminate", "Terminated"),
            ("cancel", "Cancelled"),
        ],
        related="contract_id.state",
        store=True,
        readonly=True,
    )
    invoice_id = fields.Many2one(
        string="# Invoice",
        comodel_name="account.invoice",
        readonly=True,
        ondelete="restrict",
    )
    invoice_state = fields.Selection(
        string="Invoice State",
        selection=[
            ("tobeinvoiced", "To Be Invoiced"),
            ("invoiced", "Invoiced"),
        ],
        compute="_compute_invoice_state",
        store=True,
        readonly=True,
    )
    timesheet_ids = fields.One2many(
        string="Timesheet Details",
        comodel_name="hr.analytic.timesheet",
        compute="_compute_timesheet_ids",
        store=False,
    )
    prepaid_total = fields.Float(
        string="Prepaid Total",
        compute="_compute_man_hour",
        store=True,
    )
    prepaid_usage = fields.Float(
        string="Prepaid Usage",
        compute="_compute_man_hour",
        store=True,
    )
    prepaid_diff = fields.Float(
        string="Prepaid Diff",
        compute="_compute_man_hour",
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
    def _update_analytic_account(self):
        self.ensure_one()
        if self.analytic_account_id:
            self.analytic_account_id.write(self._prepare_analytic_account())
        else:
            self._create_analytic_account()

    @api.multi
    def _create_analytic_account(self):
        self.ensure_one()
        obj_aa = self.env["account.analytic.account"]
        aa = obj_aa.create(self._prepare_analytic_account())
        self.write(
            {
                "analytic_account_id": aa.id,
            }
        )

    @api.multi
    def _prepare_analytic_account(self):
        self.ensure_one()
        contract = self.contract_id
        parent = contract.analytic_account_id
        name = "{} - {}".format(contract.name, self.name)
        return {
            "name": name,
            "type": "normal",
            "parent_id": parent and parent.id or False,
            "partner_id": contract.partner_id.id,
            "use_timesheets": True,
        }

    @api.multi
    def action_create_invoice(self):
        for record in self:
            record._create_invoice()

    @api.multi
    def action_delete_invoice(self):
        for record in self:
            record._delete_invoice()

    @api.multi
    def _create_invoice(self):
        self.ensure_one()
        invoice = self.env["account.invoice"].create(self._prepare_invoice_data())
        self.write(
            {
                "invoice_id": invoice.id,
            }
        )
        invoice.button_reset_taxes()

    @api.multi
    def _get_receivable_journal(self):
        self.ensure_one()
        contract = self.contract_id
        return contract.man_hour_receivable_journal_id

    @api.multi
    def _get_receivable_account(self):
        self.ensure_one()
        contract = self.contract_id
        return contract.man_hour_receivable_account_id

    @api.multi
    def _prepare_invoice_data(self):
        self.ensure_one()
        contract = self.contract_id
        journal = self._get_receivable_journal()
        account = self._get_receivable_account()
        invoice_line = [
            (
                0,
                0,
                {
                    "name": self.product_id.name,
                    "product_id": self.product_id.id,
                    "account_id": self.product_id.property_account_income.id,  # TODO
                    "quantity": self.quantity,
                    "uos_id": self.uom_id.id,
                    "price_unit": self.price_unit,
                    "invoice_line_tax_id": [(6, 0, self.tax_ids.ids)],
                    "account_analytic_id": self.analytic_account_id.id,
                },
            )
        ]
        return {
            "partner_id": contract.partner_id.id,
            "date_invoice": False,
            "journal_id": journal.id,
            "account_id": account.id,
            "currency_id": contract.currency_id.id,
            "origin": contract.name,
            "name": contract.title,
            "invoice_line": invoice_line,
        }

    @api.multi
    def _delete_invoice(self):
        self.ensure_one()
        invoice = self.invoice_id
        self.write(
            {
                "invoice_id": False,
            }
        )
        invoice.unlink()
