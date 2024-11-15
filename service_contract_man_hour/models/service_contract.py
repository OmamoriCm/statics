# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ServiceContract(models.Model):
    _name = "service.contract"
    _inherit = "service.contract"

    man_hour_receivable_journal_id = fields.Many2one(
        string="Man Hour Receivable Journal",
        comodel_name="account.journal",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    man_hour_receivable_account_id = fields.Many2one(
        string="Man Hour Receivable Account",
        comodel_name="account.account",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    man_hour_allowed_product_ids = fields.Many2many(
        string="Man Hour Allowed Products",
        comodel_name="product.product",
        related="type_id.man_hour_allowed_product_ids",
    )
    man_hour_allowed_product_categ_ids = fields.Many2many(
        string="Man Hour Allowed Product Categories",
        comodel_name="product.category",
        related="type_id.man_hour_allowed_product_categ_ids",
    )
    man_hour_ids = fields.One2many(
        string="Recurring Item",
        comodel_name="service.contract_man_hour",
        inverse_name="contract_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    man_hour_ok = fields.Boolean(
        string="Man Hour?",
        default=False,
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
            record._update_man_hour_analytic_account()

    @api.multi
    def _update_man_hour_analytic_account(self):
        self.ensure_one()
        for period in self.man_hour_ids:
            period._update_analytic_account()

    @api.onchange(
        "type_id",
    )
    def onchange_man_hour_receivable_journal_id(self):
        self.man_hour_receivable_journal_id = False
        if self.type_id:
            self.man_hour_receivable_journal_id = (
                self.type_id.man_hour_receivable_journal_id
            )

    @api.onchange(
        "type_id",
    )
    def onchange_man_hour_receivable_account_id(self):
        self.man_hour_receivable_account_id = False
        if self.type_id:
            self.man_hour_receivable_account_id = (
                self.type_id.man_hour_receivable_account_id
            )

    @api.onchange(
        "type_id",
    )
    def onchange_man_hour_ok(self):
        self.man_hour_ok = False
        if self.type_id:
            self.man_hour_ok = self.type_id.man_hour_ok
