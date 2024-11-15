# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil import relativedelta
from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class ServiceContract(models.Model):
    _name = "service.contract"
    _inherit = "service.contract"

    @api.depends(
        "recurring_period_num",
        "recurring_item_ids.price_unit",
        "recurring_item_ids.quantity",
        "recurring_item_ids.tax_ids",
    )
    @api.multi
    def _compute_recurring_item_total(self):
        for record in self:
            amount_untaxed = amount_tax = amount_total = 0.0
            for item in record.recurring_item_ids:
                amount_untaxed += item.amount_untaxed
                amount_tax += item.amount_tax
                amount_total += item.amount_total
            record.recurring_item_amount_untaxed = amount_untaxed
            record.recurring_item_amount_tax = amount_tax
            record.recurring_item_amount_total = amount_total

    recurring_item_amount_untaxed = fields.Float(
        string="Total Recurring Item Amount Untaxed",
        compute="_compute_recurring_item_total",
        store=True,
    )
    recurring_item_amount_tax = fields.Float(
        string="Total Recurring Item Amount Tax",
        compute="_compute_recurring_item_total",
        store=True,
    )
    recurring_item_amount_total = fields.Float(
        string="Total Recurring Item Amount Total",
        compute="_compute_recurring_item_total",
        store=True,
    )
    recurring_item_receivable_journal_id = fields.Many2one(
        string="Recurring Item Receivable Journal",
        comodel_name="account.journal",
    )
    recurring_item_receivable_account_id = fields.Many2one(
        string="Recurring Item Receivable Account",
        comodel_name="account.account",
    )
    recurring_item_income_realization_account_id = fields.Many2one(
        string="Recurring Item Income Realization Account",
        comodel_name="account.account",
    )
    recurring_item_income_realization_journal_id = fields.Many2one(
        string="Recurring Item Income Realization Journal",
        comodel_name="account.journal",
    )
    recurring_item_allowed_product_ids = fields.Many2many(
        string="Recurring Item Allowed Products",
        comodel_name="product.product",
        related="type_id.recurring_item_allowed_product_ids",
    )
    recurring_item_allowed_product_categ_ids = fields.Many2many(
        string="Recurring Item Allowed Product Categories",
        comodel_name="product.category",
        related="type_id.recurring_item_allowed_product_categ_ids",
    )
    recurring_item_ids = fields.One2many(
        string="Recurring Item",
        comodel_name="service.contract_recurring_item",
        inverse_name="contract_id",
        readonly=False,
    )
    recurring_service_ok = fields.Boolean(
        string="Recurring Service?",
        default=False,
    )
    recurring_period_ids = fields.One2many(
        string="Recurring Period",
        comodel_name="service.contract_recurring_period",
        inverse_name="contract_id",
        readonly=True,
    )
    recurring_period = fields.Integer(
        string="Recurring Service Period",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    recurring_period_lenght = fields.Selection(
        string="Recurring Service Period Lenght",
        selection=[
            ("month", "Monthly"),
        ],
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    recurring_period_num = fields.Integer(
        string="Recurring Service Period Number",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.multi
    def action_approve(self):
        _super = super(ServiceContract, self)
        _super.action_approve()
        for record in self:
            record._update_recurring_period_analytic_account()

    @api.multi
    def action_reload_recurring_item_price(self):
        for record in self:
            record._reload_recurring_item_price()

    @api.multi
    def action_create_recurring_period(self):
        for record in self:
            record._delete_recurring_period()
            record._create_recurring_period()

    @api.multi
    def _reload_recurring_item_price(self):
        self.ensure_one()
        for recurring_item in self.recurring_item_ids:
            recurring_item.onchange_price_unit()

    @api.multi
    def _update_recurring_period_analytic_account(self):
        self.ensure_one()
        for period in self.recurring_period_ids:
            period._update_analytic_account()

    @api.multi
    def _delete_recurring_period(self):
        self.ensure_one()
        for period in self.recurring_period_ids:
            aa = period.analytic_account_id
            period.write({"analytic_account_id": False})
            aa.unlink()
        self.recurring_period_ids.unlink()

    @api.multi
    def _create_recurring_period(self):
        self.ensure_one()

        obj_recurring_period = self.env["service.contract_recurring_period"]
        date_start = self.date_start
        for _period_num in range(1, self.recurring_period_num + 1):
            date_end = self._get_recurring_period_date_end(date_start)
            data = {
                "contract_id": self.id,
                "date_start": date_start,
                "date_end": date_end,
            }
            obj_recurring_period.create(data)
            date_start = self._get_recurring_period_date_start(date_end)

    @api.multi
    def _get_recurring_period_date_end(self, date_start):
        self.ensure_one()

        dt_start = fields.Date.from_string(date_start)
        date_end = dt_start + relativedelta.relativedelta(
            months=self.recurring_period, days=-1
        )
        return fields.Date.to_string(date_end)

    @api.multi
    def _get_recurring_period_date_start(self, date_end):
        self.ensure_one()

        dt_end = fields.Date.from_string(date_end)
        date_start = dt_end + relativedelta.relativedelta(days=1)
        return fields.Date.to_string(date_start)

    @api.onchange(
        "type_id",
    )
    def onchange_recurring_item_receivable_journal_id(self):
        self.recurring_item_receivable_journal_id = False
        if self.type_id:
            self.recurring_item_receivable_journal_id = (
                self.type_id.recurring_item_receivable_journal_id
            )

    @api.onchange(
        "type_id",
    )
    def onchange_recurring_item_receivable_account_id(self):
        self.recurring_item_receivable_account_id = False
        if self.type_id:
            self.recurring_item_receivable_account_id = (
                self.type_id.recurring_item_receivable_account_id
            )

    @api.onchange(
        "type_id",
    )
    def onchange_recurring_service_ok(self):
        self.recurring_service_ok = False
        if self.type_id:
            self.recurring_service_ok = self.type_id.recurring_service_ok

    @api.constrains(
        "state",
    )
    def constrains_confirm(self):
        msg_error = _(
            "Number Recurring Service Period Number "
            "Must Equal With Number of Record on Recurring Period"
        )
        for record in self:
            if record.state == "confirm" and not record._check_number_reccurring():
                raise UserError(msg_error)

    @api.multi
    def _check_number_reccurring(self):
        self.ensure_one()
        result = True
        obj_term = self.env["service.contract_recurring_period"]
        criteria = [("contract_id", "=", self.id)]
        count = obj_term.search_count(criteria)
        if count != self.recurring_period_num:
            result = False
        return result
