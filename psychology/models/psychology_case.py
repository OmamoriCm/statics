# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class PsychologyCase(models.Model):
    _name = "psychology.case"
    _description = "Psychology Case"
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
        "base.terminate.reason_common",
    ]
    _state_from = ["draft", "confirm"]
    _state_to = ["open"]

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    @api.multi
    def _compute_policy(self):
        _super = super(PsychologyCase, self)
        _super._compute_policy()

    @api.depends(
        "service_ids",
        "service_ids.case_id",
    )
    @api.multi
    def _compute_service_count(self):
        obj_service = self.env["psychology.case_service"]
        for record in self:
            criteria = [("case_id", "=", record.id)]
            record.service_count = obj_service.search_count(criteria)

    @api.depends(
        "activity_ids",
        "activity_ids.case_id",
    )
    @api.multi
    def _compute_activity_count(self):
        obj_activity = self.env["psychology.case_activity"]
        for record in self:
            criteria = [("case_id", "=", record.id)]
            record.activity_count = obj_activity.search_count(criteria)

    @api.depends(
        "customer_invoice_ids",
    )
    @api.multi
    def _compute_customer_invoice_count(self):
        for record in self:
            record.customer_invoice_count = len(record.customer_invoice_ids)

    @api.depends(
        "supplier_invoice_ids",
    )
    @api.multi
    def _compute_supplier_invoice_count(self):
        for record in self:
            record.supplier_invoice_count = len(record.supplier_invoice_ids)

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
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
    )
    partner_id = fields.Many2one(
        string="Client",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_psychologist_ids = fields.Many2many(
        string="Allowed Psychologist",
        comodel_name="res.partner",
        related="type_id.allowed_psychologist_ids",
        store=False,
    )
    psychologist_id = fields.Many2one(
        string="Psychologist",
        comodel_name="res.partner",
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
        comodel_name="psychology.case_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    # Service Related Fields
    service_allowed_product_ids = fields.Many2many(
        string="Service Allowed Products",
        comodel_name="product.product",
        related="type_id.service_allowed_product_ids",
        store=False,
    )
    service_allowed_product_categ_ids = fields.Many2many(
        string="Fix Item Allowed Product Categories",
        comodel_name="product.category",
        related="type_id.service_allowed_product_categ_ids",
        store=False,
    )
    service_ids = fields.One2many(
        string="Services",
        comodel_name="psychology.case_service",
        inverse_name="case_id",
        readonly=True,
    )
    service_count = fields.Integer(
        string="Num. of Service",
        compute="_compute_service_count",
        store=True,
    )
    service_pricelist_id = fields.Many2one(
        string="Service Pricelist",
        comodel_name="product.pricelist",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    customer_invoice_ids = fields.Many2many(
        string="Customer Invoices",
        comodel_name="account.invoice",
        relation="rel_psychology_case_2_customer_invoice",
        column1="case_id",
        column2="invoice_id",
    )
    customer_invoice_count = fields.Integer(
        string="Num. of Customer Invoice",
        compute="_compute_customer_invoice_count",
        store=True,
    )
    # Activity Related Fields
    activity_ids = fields.One2many(
        string="Activities",
        comodel_name="psychology.case_activity",
        inverse_name="case_id",
        readonly=True,
    )
    activity_count = fields.Integer(
        string="Num. of Activity",
        compute="_compute_activity_count",
        store=True,
    )
    activity_allowed_product_ids = fields.Many2many(
        string="Activity Allowed Products",
        comodel_name="product.product",
        related="type_id.service_allowed_product_ids",
        store=False,
    )
    activity_allowed_product_categ_ids = fields.Many2many(
        string="Activity Allowed Product Categories",
        comodel_name="product.category",
        related="type_id.service_allowed_product_categ_ids",
        store=False,
    )
    activity_pricelist_id = fields.Many2one(
        string="Activity Pricelist",
        comodel_name="product.pricelist",
        required=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    supplier_invoice_ids = fields.Many2many(
        string="Supplier Invoices",
        comodel_name="account.invoice",
        relation="rel_psychology_case_2_supplier_invoice",
        column1="case_id",
        column2="invoice_id",
    )
    supplier_invoice_count = fields.Integer(
        string="Num. of Supplier Invoice",
        compute="_compute_supplier_invoice_count",
        store=True,
    )
    note = fields.Text(
        string="Note",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )
    # Log Files
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
        string="Open Date",
        readonly=True,
        copy=False,
    )
    open_user_id = fields.Many2one(
        string="Opened By",
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
        string="Done By",
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
        string="Can Open",
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
    out_invoice_ok = fields.Boolean(
        string="Can Create Customer Invoice From Service",
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

    @api.multi
    def action_finish(self):
        for record in self:
            record.write(record._prepare_finish_data())

    @api.multi
    def action_cancel(self):
        for record in self:
            record.write(record._prepare_cancel_data())

    @api.multi
    def action_restart(self):
        for record in self:
            record.write(record._prepare_restart_data())

    @api.multi
    def action_open_service(self):
        self.ensure_one()
        waction = self.env.ref("psychology.psychology_case_service_action")
        waction = waction.read()[0]
        waction.update(
            {
                "domain": [("case_id", "=", self.id)],
                "context": {
                    "default_pricelist_id": self.service_pricelist_id.id,
                    "default_case_id": self.id,
                },
            }
        )
        return waction

    @api.multi
    def action_open_customer_invoice(self):
        self.ensure_one()
        waction = self.env.ref("account.action_invoice_tree1")
        waction = waction.read()[0]
        waction.update(
            {
                "domain": [("id", "in", self.customer_invoice_ids.ids)],
            }
        )
        return waction

    @api.multi
    def action_open_supplier_invoice(self):
        self.ensure_one()
        waction = self.env.ref("account.action_invoice_tree2")
        waction = waction.read()[0]
        waction.update(
            {
                "domain": [("id", "in", self.supplier_invoice_ids.ids)],
            }
        )
        return waction

    @api.multi
    def action_open_activity(self):
        self.ensure_one()
        waction = self.env.ref("psychology.psychology_case_activity_action")
        waction = waction.read()[0]
        waction.update(
            {
                "domain": [("case_id", "=", self.id)],
                "context": {
                    "default_pricelist_id": self.activity_pricelist_id.id,
                    "default_case_id": self.id,
                },
            }
        )
        return waction

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
        return {
            "state": "open",
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
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
            "confirm_date": False,
            "confirm_user_id": False,
            "done_date": False,
            "done_user_id": False,
            "cancel_date": False,
            "cancel_user_id": False,
        }

    @api.onchange(
        "type_id",
    )
    def onchange_service_pricelist_id(self):
        self.service_pricelist_id = False
        if self.type_id:
            self.service_pricelist_id = self.type_id.service_pricelist_id

    @api.onchange(
        "type_id",
    )
    def onchange_activity_pricelist_id(self):
        self.activity_pricelist_id = False
        if self.type_id:
            self.activity_pricelist_id = self.type_id.activity_pricelist_id

    @api.multi
    def _create_supplier_invoice(self, activity_ids, date_invoice=False):
        self.ensure_one()
        obj_invoice = self.env["account.invoice"]
        partners = activity_ids.mapped("responsible_id")
        supplier_invoice_ids = []
        for partner in partners:
            invoice = obj_invoice.create(
                self._prepare_supplier_invoice_data(
                    partner=partner, date_invoice=date_invoice
                )
            )
            activities = activity_ids.filtered(
                lambda r: r.responsible_id.id == partner.id
            )
            for activity in activities:
                activity._create_supplier_invoice_line(invoice)

            supplier_invoice_ids.append(invoice.id)

        supplier_invoice_ids = self.supplier_invoice_ids.ids + supplier_invoice_ids
        self.write({"supplier_invoice_ids": [(6, 0, supplier_invoice_ids)]})

    @api.multi
    def _prepare_supplier_invoice_data(self, partner, date_invoice=False):
        self.ensure_one()
        journal = self._get_service_payable_journal()
        account = self._get_service_payable_account()
        currency = self.activity_pricelist_id.currency_id
        return {
            "partner_id": partner.id,
            "date_invoice": date_invoice,
            "journal_id": journal.id,
            "account_id": account.id,
            "currency_id": currency.id,
            "origin": self.name,
            "name": self.name,
            "type": "in_invoice",
        }

    @api.multi
    def _get_service_payable_journal(self):
        self.ensure_one()
        result = self.type_id.payable_journal_id
        return result

    @api.multi
    def _get_service_payable_account(self):
        self.ensure_one()
        result = self.type_id.payable_account_id
        return result

    @api.multi
    def _unlink_supplier_invoice(self, invoice):
        self.ensure_one()
        obj_activity = self.env["psychology.case_activity"]
        criteria = [
            ("invoice_id", "=", invoice.id),
        ]
        activities = obj_activity.search(criteria)
        activities.write({"invoice_line_id": False, "invoice_state": "2binvoiced"})
        invoice.unlink()

    @api.multi
    def _create_customer_invoice(self, service_ids, date_invoice=False):
        self.ensure_one()
        obj_invoice = self.env["account.invoice"]
        invoice = obj_invoice.create(self._prepare_customer_invoice_data(date_invoice))
        for service in service_ids:
            service._create_customer_invoice_line(invoice)
        customer_invoice_ids = self.customer_invoice_ids.ids + [invoice.id]
        self.write({"customer_invoice_ids": [(6, 0, customer_invoice_ids)]})

    @api.multi
    def _get_service_receivable_journal(self):
        self.ensure_one()
        result = self.type_id.receivable_journal_id
        return result

    @api.multi
    def _get_service_receivable_account(self):
        self.ensure_one()
        result = self.type_id.receivable_account_id
        return result

    @api.multi
    def _prepare_customer_invoice_data(self, date_invoice=False):
        self.ensure_one()
        journal = self._get_service_receivable_journal()
        account = self._get_service_receivable_account()
        currency = self.service_pricelist_id.currency_id
        return {
            "partner_id": self.partner_id.id,
            "date_invoice": date_invoice,
            "journal_id": journal.id,
            "account_id": account.id,
            "currency_id": currency.id,
            "origin": self.name,
            "name": self.name,
            "type": "out_invoice",
        }

    @api.multi
    def _unlink_customer_invoice(self, invoice):
        self.ensure_one()
        obj_service = self.env["psychology.case_service"]
        criteria = [("invoice_id", "=", invoice.id), ("case_id", "=", self.id)]
        services = obj_service.search(criteria)
        services.write({"invoice_line_id": False, "invoice_state": "2binvoiced"})
        invoice.unlink()

    @api.model
    def create(self, values):
        _super = super(PsychologyCase, self)
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
        _super = super(PsychologyCase, self)
        _super.unlink()

    @api.multi
    def validate_tier(self):
        _super = super(PsychologyCase, self)
        _super.validate_tier()
        for record in self:
            if record.validated:
                record.action_approve()

    @api.multi
    def restart_validation(self):
        _super = super(PsychologyCase, self)
        _super.restart_validation()
        for record in self:
            record.request_validation()

    @api.onchange(
        "type_id",
    )
    def onchange_psychologist_id(self):
        self.psychologist_id = False
