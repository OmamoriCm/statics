# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models


class HrReimbursementLine(models.Model):
    _name = "hr.reimbursement_line"
    _description = "Employee Reimbursement Line"

    @api.depends(
        "approve_quantity",
        "approve_price_unit",
    )
    @api.multi
    def _compute_price_subtotal(self):
        for document in self:
            document.price_subtotal = (
                document.approve_quantity * document.approve_price_unit
            )

    @api.depends(
        "product_id",
    )
    @api.multi
    def _compute_allowed_uom_ids(self):
        obj_uom = self.env["product.uom"]
        for document in self:
            result = []
            if document.product_id:
                categ = document.product_id.uom_id.category_id
                criteria = [
                    ("category_id", "=", categ.id),
                ]
                result = obj_uom.search(criteria).ids
            document.allowed_uom_ids = result

    reimbursement_id = fields.Many2one(
        string="# Reimbursement",
        comodel_name="hr.reimbursement",
        ondelete="cascade",
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        related="reimbursement_id.employee_id",
        store=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
    )
    note = fields.Text(
        string="Note",
    )
    ref = fields.Char(
        string="Reference",
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        domain=[
            ("type", "=", "other"),
        ],
        required=True,
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
    )
    price_unit = fields.Float(
        string="Unit Price",
        required=True,
    )
    approve_price_unit = fields.Float(
        string="Approved Price Unit",
        readonly=True,
    )
    quantity = fields.Float(
        string="Qty",
        required=True,
        default=1.0,
    )
    approve_quantity = fields.Float(
        string="Approved Quantity",
        readonly=True,
    )
    allowed_uom_ids = fields.Many2many(
        string="Allowed UoM",
        comodel_name="product.uom",
        compute="_compute_allowed_uom_ids",
        store=False,
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
        required=True,
    )
    price_subtotal = fields.Float(
        string="Subtotal",
        compute="_compute_price_subtotal",
        store=True,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="hr.reimbursement_type",
        related="reimbursement_id.type_id",
        store=False,
    )
    reimbursement_state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("approve", "Waiting for Realization"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        related="reimbursement_id.state",
        store=False,
    )

    @api.onchange(
        "product_id",
    )
    def onchange_uom_id(self):
        self.uom_id = False
        if self.product_id:
            self.uom_id = self.product_id.uom_id

    @api.onchange(
        "quantity",
    )
    def onchange_approve_quantity(self):
        self.approve_quantity = self.quantity

    @api.onchange(
        "price_unit",
    )
    def onchange_approve_price_unit(self):
        self.approve_price_unit = self.price_unit

    @api.onchange(
        "product_id",
    )
    def onchange_account_id(self):
        result = False

        if self.product_id:
            result = self.product_id.property_account_expense

        if self.product_id and not result:
            result = self.product_id.categ_id.property_account_expense_categ

        self.account_id = result

    @api.multi
    def _create_expense_move_line(self):
        self.ensure_one()
        obj_line = self.env["account.move.line"]
        obj_line.create(self._prepare_expense_move_lines())

    @api.multi
    def _prepare_expense_move_lines(self):
        self.ensure_one()
        reimbusement = self.reimbursement_id
        currency = reimbusement._get_currency()
        debit, credit, amount_currency = self._get_expense_amount()
        move_name = _(
            "Employee reimbursement %s: %s - %s"
            % (reimbusement.name, self.product_id.name, self.note)
        )
        aa = self.analytic_account_id
        return {
            "name": move_name,
            "move_id": reimbusement.move_id.id,
            "partner_id": reimbusement._get_partner().id,
            "account_id": self.account_id.id,
            "product_id": self.product_id.id,
            "quantity": self.approve_quantity,
            "credit": credit,
            "debit": debit,
            "currency_id": currency and currency.id or False,
            "amount_currency": amount_currency,
            "analytic_account_id": aa and aa.id or False,
        }

    @api.multi
    def _get_expense_amount(self):
        debit = credit = amount = amount_currency = 0.0
        reimbusement = self.reimbursement_id
        currency = reimbusement._get_currency()
        move_date = reimbusement.date_expense
        if currency:
            amount_currency = self.price_subtotal
            amount = currency.with_context(date=move_date).compute(
                amount_currency,
                reimbusement.company_id.currency_id,
            )
        else:
            amount = self.price_subtotal

        if amount >= 0.0:
            debit = amount
        else:
            credit = amount
            amount_currency *= -1.0

        return debit, credit, amount_currency
