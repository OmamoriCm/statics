# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class ServiceContract(models.Model):
    _name = "service.contract"
    _description = "Service Contract"
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
        "base.terminate.reason_common",
        "custom.info.mixin",
    ]
    _state_from = ["draft", "confirm"]
    _state_to = ["approve"]

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_currency_id(self):
        return self.env.user.company_id.currency_id.id

    @api.multi
    def _compute_policy(self):
        _super = super(ServiceContract, self)
        _super._compute_policy()

    @api.depends(
        "fix_item_payment_term_ids",
        "fix_item_payment_term_ids.amount_untaxed",
        "fix_item_payment_term_ids.amount_tax",
        "fix_item_payment_term_ids.amount_total",
    )
    @api.multi
    def _compute_fix_item_total(self):
        for record in self:
            amount_untaxed = amount_tax = amount_total = 0.0
            for fix_item in record.fix_item_payment_term_ids:
                amount_untaxed += fix_item.amount_untaxed
                amount_tax += fix_item.amount_tax
                amount_total += fix_item.amount_total
            record.amount_untaxed = amount_untaxed
            record.amount_tax = amount_tax
            record.amount_total = amount_total

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    title = fields.Char(
        string="Title",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    reference = fields.Char(
        string="Reference",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    partner_signee_id = fields.Many2one(
        string="Signee",
        comodel_name="res.partner",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    partner_invoice_id = fields.Many2one(
        string="Invoice To",
        comodel_name="res.partner",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    partner_contact_id = fields.Many2one(
        string="Contact Person",
        comodel_name="res.partner",
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
        default=lambda self: self._default_currency_id(),
        required=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    salesman_id = fields.Many2one(
        string="Salesman",
        comodel_name="res.users",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    responsible_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="service.contract_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date = fields.Date(
        string="Contract Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_start = fields.Date(
        string="Date Start",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_end = fields.Date(
        string="Date End",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    parent_analytic_account_id = fields.Many2one(
        string="Parent Analytic Account",
        comodel_name="account.analytic.account",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
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
    fix_item_ids = fields.One2many(
        string="Fixed Items",
        comodel_name="service.contract_fix_item",
        inverse_name="contract_id",
        readonly=True,
    )
    amount_untaxed = fields.Float(
        string="Untaxed",
        required=False,
        compute="_compute_fix_item_total",
        store=False,
    )
    amount_tax = fields.Float(
        string="Tax",
        required=False,
        compute="_compute_fix_item_total",
        store=False,
    )
    amount_total = fields.Float(
        string="Total",
        required=False,
        compute="_compute_fix_item_total",
        store=False,
    )
    fix_item_receivable_journal_id = fields.Many2one(
        string="Fix Item Receivable Journal",
        comodel_name="account.journal",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    fix_item_receivable_account_id = fields.Many2one(
        string="Fix Item Receivable Account",
        comodel_name="account.account",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    fix_item_payment_term_ids = fields.One2many(
        string="Fix Item Payment Terms",
        comodel_name="service.contract_fix_item_payment_term",
        inverse_name="contract_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        copy=True,
    )
    fix_item_allowed_product_ids = fields.Many2many(
        string="Fix Item Allowed Products",
        comodel_name="product.product",
        related="type_id.fix_item_allowed_product_ids",
        store=False,
    )
    fix_item_allowed_product_categ_ids = fields.Many2many(
        string="Fix Item Allowed Product Categories",
        comodel_name="product.category",
        related="type_id.fix_item_allowed_product_categ_ids",
        store=False,
    )
    team_function_allowed_product_ids = fields.Many2many(
        string="Team Function Allowed Products",
        comodel_name="product.product",
        related="type_id.team_function_allowed_product_ids",
        store=False,
    )
    team_function_allowed_product_categ_ids = fields.Many2many(
        string="Team Function Allowed Product Categories",
        comodel_name="product.category",
        related="type_id.team_function_allowed_product_categ_ids",
        store=False,
    )
    team_ids = fields.One2many(
        string="Teams",
        comodel_name="service.contract_team",
        inverse_name="contract_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    note = fields.Text(
        string="Note",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("approve", "Ready to Start"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("terminate", "Terminated"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )
    confirm_date = fields.Datetime(
        string="Confirmation Date",
        readonly=True,
        copy=False,
    )
    confirm_user_id = fields.Many2one(
        string="Confirmed By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    open_date = fields.Datetime(
        string="Start Date",
        readonly=True,
        copy=False,
    )
    open_user_id = fields.Many2one(
        string="Start By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    done_date = fields.Datetime(
        string="Finish Date",
        readonly=True,
        copy=False,
    )
    done_user_id = fields.Many2one(
        string="Finished By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    cancel_date = fields.Datetime(
        string="Cancel Date",
        readonly=True,
        copy=False,
    )
    cancel_user_id = fields.Many2one(
        string="Cancelled By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    terminate_date = fields.Datetime(
        string="Terminate Date",
        readonly=True,
        copy=False,
    )
    terminate_user_id = fields.Many2one(
        string="Terminated By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    # Policy Field
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    restart_approval_ok = fields.Boolean(
        string="Can Restart Approval",
        compute="_compute_policy",
    )
    open_ok = fields.Boolean(
        string="Can Force Start",
        compute="_compute_policy",
    )
    finish_ok = fields.Boolean(
        string="Can Force Finish",
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
    terminate_ok = fields.Boolean(
        string="Can Terminate",
        compute="_compute_policy",
    )

    @api.multi
    def action_confirm(self):
        for record in self:
            record.write(record._prepare_confirm_data())
            record.request_validation()

    @api.multi
    def action_approve(self):
        for record in self:
            record.write(record._prepare_approve_data())
            record._create_analytic_account()

    @api.multi
    def action_start(self):
        for record in self:
            record.write(record._prepare_start_data())

    @api.multi
    def action_finish(self):
        for record in self:
            record.write(record._prepare_finish_data())

    @api.multi
    def action_cancel(self):
        for record in self:
            record.write(record._prepare_cancel_data())

    @api.multi
    def action_terminate(self):
        for record in self:
            record.write(record._prepare_terminate_data())

    @api.multi
    def action_restart(self):
        for record in self:
            record.write(record._prepare_restart_data())

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirm",
            "confirm_date": fields.Datetime.now(),
            "confirm_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_approve_data(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.update(
            {
                "ir_sequence_date": self.date,
            }
        )
        sequence = self.with_context(ctx)._create_sequence()
        return {
            "state": "approve",
            "name": sequence,
        }

    @api.multi
    def _prepare_start_data(self):
        self.ensure_one()
        return {
            "state": "open",
            "open_date": fields.Datetime.now(),
            "open_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_finish_data(self):
        self.ensure_one()
        return {
            "state": "done",
            "done_date": fields.Datetime.now(),
            "done_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
            "cancel_date": fields.Datetime.now(),
            "cancel_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_terminate_data(self):
        self.ensure_one()
        return {
            "state": "terminate",
            "terminate_date": fields.Datetime.now(),
            "terminate_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
            "confirm_date": False,
            "confirm_user_id": False,
            "open_date": False,
            "open_user_id": False,
            "done_date": False,
            "done_user_id": False,
            "cancel_date": False,
            "cancel_user_id": False,
            "terminate_date": False,
            "terminate_user_id": False,
        }

    @api.onchange(
        "type_id",
    )
    def onchange_fix_item_receivable_journal_id(self):
        self.fix_item_receivable_journal_id = False
        if self.type_id:
            self.fix_item_receivable_journal_id = (
                self.type_id.fix_item_receivable_journal_id
            )

    @api.onchange(
        "type_id",
    )
    def onchange_fix_item_receivable_account_id(self):
        self.fix_item_receivable_account_id = False
        if self.type_id:
            self.fix_item_receivable_account_id = (
                self.type_id.fix_item_receivable_account_id
            )

    @api.onchange(
        "currency_id",
    )
    def onchange_pricelist_id(self):
        self.pricelist_id = False

    @api.onchange(
        "partner_id",
    )
    def onchange_partner_signee_id(self):
        self.partner_signee_id = False

    @api.onchange(
        "partner_id",
    )
    def onchange_partner_contact_id(self):
        self.partner_contact_id = False

    @api.onchange(
        "partner_id",
    )
    def onchange_partner_invoice_id(self):
        self.partner_invoice_id = False

    @api.onchange(
        "type_id",
    )
    def onchange_parent_analytic_account_id(self):
        self.parent_analytic_account_id = False
        if self.type_id:
            self.parent_analytic_account_id = self.type_id.parent_analytic_account_id

    @api.onchange(
        "type_id",
    )
    def onchange_custom_info_template_id(self):
        self.custom_info_template_id = False
        if self.type_id:
            self.custom_info_template_id = self.type_id.contract_custom_info_template_id

    @api.multi
    def _create_analytic_account(self):
        self.ensure_one()
        if self.analytic_account_id:
            self._update_analytic_account()
        else:
            obj_aa = self.env["account.analytic.account"]
            aa = obj_aa.create(self._prepare_analytic_account())
            self.write(
                {
                    "analytic_account_id": aa.id,
                }
            )

    @api.multi
    def _update_analytic_account(self):
        self.ensure_one()
        self.analytic_account_id.write(self._prepare_update_analytic_account())

    @api.multi
    def _prepare_update_analytic_account(self):
        self.ensure_one()
        parent = self.parent_analytic_account_id
        return {
            "name": self.title,
            "code": self.name,
            "type": "normal",
            "parent_id": parent and parent.id or False,
            "partner_id": self.partner_id.id,
            "date_start": self.date_start,
            "date": self.date_end or False,
            "manager_id": self.responsible_id.id,
        }

    @api.multi
    def _prepare_analytic_account(self):
        self.ensure_one()
        parent = self.parent_analytic_account_id
        return {
            "name": self.title,
            "code": self.name,
            "type": "normal",
            "parent_id": parent and parent.id or False,
            "partner_id": self.partner_id.id,
            "date_start": self.date_start,
            "date": self.date_end or False,
            "manager_id": self.responsible_id.id,
        }

    @api.constrains(
        "state",
    )
    def constrains_cancel(self):
        msg_error = _("Please delete all payment term invoice")
        for record in self:
            if (
                record.state == "cancel"
                and not record._check_all_payment_term_uninvoiced()
            ):
                raise UserError(msg_error)

    @api.multi
    def _check_all_payment_term_uninvoiced(self):
        self.ensure_one()
        result = True
        obj_term = self.env["service.contract_fix_item_payment_term"]
        criteria = [("contract_id", "=", self.id), ("invoice_id", "!=", False)]
        count = obj_term.search_count(criteria)
        if count > 0:
            result = False
        return result

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for record in self:
            if record.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(ServiceContract, self)
        _super.unlink()

    @api.multi
    def validate_tier(self):
        _super = super(ServiceContract, self)
        _super.validate_tier()
        for record in self:
            if record.validated:
                record.action_approve()

    @api.multi
    def restart_validation(self):
        _super = super(ServiceContract, self)
        _super.restart_validation()
        for record in self:
            record.request_validation()

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.name == "/":
                name = "*" + str(record.id)
            else:
                name = record.name
            result.append((record.id, name))
        return result
