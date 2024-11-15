# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class HrReimbursement(models.Model):
    _name = "hr.reimbursement"
    _description = "Employee Reimbursement"
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
        "base.terminate.reason_common",
    ]
    _state_from = ["draft", "confirm"]
    _state_to = ["approve"]

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_currency_id(self):
        return self.env.user.company_id.currency_id.id

    @api.model
    def _default_employee_id(self):
        employees = self.env.user.employee_ids
        if len(employees) > 0:
            return employees[0].id

    @api.depends(
        "line_ids",
        "line_ids.price_subtotal",
    )
    @api.multi
    def _compute_amount_total(self):
        for document in self:
            total = 0.0
            for line in document.line_ids:
                total += line.price_subtotal
            document.amount_total = total

    @api.depends(
        "employee_reimbursement_payable_move_line_id.amount_residual",
        "employee_reimbursement_payable_move_line_id",
        "employee_reimbursement_payable_move_line_id.reconcile_id",
        "employee_reimbursement_payable_move_line_id.reconcile_partial_id",
        "amount_total",
        "state",
    )
    @api.multi
    def _compute_residual(self):
        for document in self:
            realized = 0.0
            residual = document.amount_total
            currency = document._get_currency()
            if document.employee_reimbursement_payable_move_line_id:
                move_line = document.employee_reimbursement_payable_move_line_id
                if not currency:
                    residual = move_line.amount_residual
                else:
                    residual = move_line.amount_residual_currency
                realized = document.amount_total - residual
            document.amount_realized = realized
            document.amount_residual = residual

    @api.multi
    def _compute_policy(self):
        _super = super(HrReimbursement, self)
        _super._compute_policy()

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
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        default=lambda self: self._default_currency_id(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        default=lambda self: self._default_employee_id(),
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
        comodel_name="hr.reimbursement_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        related="type_id.allowed_product_categ_ids",
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Products",
        comodel_name="product.product",
        related="type_id.allowed_product_ids",
    )
    department_id = fields.Many2one(
        string="Department",
        comodel_name="hr.department",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    manager_id = fields.Many2one(
        string="Manager",
        comodel_name="hr.employee",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    job_id = fields.Many2one(
        string="Job Position",
        comodel_name="hr.job",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_expense = fields.Date(
        string="Date Expense",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_due = fields.Date(
        string="Date Due",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    amount_total = fields.Float(
        string="Total",
        compute="_compute_amount_total",
        store=True,
    )
    amount_realized = fields.Float(
        string="Total Payment",
        compute="_compute_residual",
        store=True,
    )
    amount_residual = fields.Float(
        string="Total Residual",
        compute="_compute_residual",
        store=True,
    )
    note = fields.Text(
        string="Note",
    )

    # Accounting Setting
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        domain=[
            ("type", "=", "general"),
        ],
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    employee_reimbursement_payable_account_id = fields.Many2one(
        string="Reimbursement Payable Account",
        comodel_name="account.account",
        domain=[
            ("reconcile", "=", True),
        ],
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    move_id = fields.Many2one(
        string="# Move",
        comodel_name="account.move",
        readonly=True,
        copy=False,
        ondelete="restrict",
    )
    employee_reimbursement_payable_move_line_id = fields.Many2one(
        string="Reimbursement Payable Move Line",
        comodel_name="account.move.line",
        readonly=True,
        copy=False,
        ondelete="restrict",
    )
    line_ids = fields.One2many(
        string="Reimbursement Details",
        comodel_name="hr.reimbursement_line",
        inverse_name="reimbursement_id",
        copy=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("approve", "Waiting for Payment"),
            ("done", "Done"),
            ("terminate", "Terminated"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )
    # Log Fields
    confirm_date = fields.Datetime(
        string="Confirm Date",
        readonly=True,
        copy=False,
    )
    confirm_user_id = fields.Many2one(
        string="Confirmed By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    approve_date = fields.Datetime(
        string="Approve Date",
        readonly=True,
        copy=False,
    )
    approve_user_id = fields.Many2one(
        string="Approve By",
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
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    change_detail_ok = fields.Boolean(
        string="Can Change Detail",
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
    show_accounting_info_ok = fields.Boolean(
        string="Can See Accounting Info",
        compute="_compute_policy",
    )

    @api.multi
    def action_confirm(self):
        for document in self:
            document.write(document._prepare_confirm_data())
            document.request_validation()

    @api.multi
    def action_approve(self):
        for document in self:
            document.write(document._prepare_approve_data())
            if not document.move_id:
                document._create_accounting_entry()

    @api.multi
    def action_done(self):
        for document in self:
            document.write(document._prepare_done_data())

    @api.multi
    def action_terminate(self):
        for document in self:
            document.write(document._prepare_terminate_data())

    @api.multi
    def action_cancel(self):
        for document in self:
            move = document.move_id
            document.write(document._prepare_cancel_data())
            if move:
                move.unlink()
            document.restart_validation()

    @api.multi
    def action_restart(self):
        for document in self:
            document.write(document._prepare_restart_data())

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
                "ir_sequence_date": self.date_expense,
            }
        )
        sequence = self.with_context(ctx)._create_sequence()
        return {
            "state": "approve",
            "name": sequence,
            "approve_date": fields.Datetime.now(),
            "approve_user_id": self.env.user.id,
            "done_date": False,
            "done_user_id": False,
        }

    @api.multi
    def _prepare_done_data(self):
        self.ensure_one()
        return {
            "state": "done",
            "done_date": fields.Datetime.now(),
            "done_user_id": self.env.user.id,
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
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
            "cancel_date": fields.Datetime.now(),
            "cancel_user_id": self.env.user.id,
            "move_id": False,
            "employee_reimbursement_payable_move_line_id": False,
        }

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
            "confirm_date": False,
            "confirm_user_id": False,
            "approve_date": False,
            "approve_user_id": False,
            "done_date": False,
            "done_user_id": False,
            "cancel_date": False,
            "cancel_user_id": False,
            "terminate_date": False,
            "terminate_user_id": False,
            "cancel_reason_id": False,
            "terminate_reason_id": False,
        }

    @api.multi
    def _create_accounting_entry(self):
        self.ensure_one()
        self._create_account_move()
        self._create_payable_reimbursement_move_line()
        for line in self.line_ids:
            line._create_expense_move_line()

    @api.multi
    def _create_account_move(self):
        self.ensure_one()
        obj_move = self.env["account.move"]
        move = obj_move.create(self._prepare_account_move())
        self.write({"move_id": move.id})

    @api.multi
    def _create_payable_reimbursement_move_line(self):
        self.ensure_one()
        obj_line = self.env["account.move.line"]
        line = obj_line.create(self._prepare_payable_reimbursement_move_lines())
        self.write({"employee_reimbursement_payable_move_line_id": line.id})

    @api.multi
    def _get_currency(self):
        self.ensure_one()
        result = False
        if self.company_id.currency_id != self.currency_id:
            result = self.currency_id
        return result

    @api.multi
    def _get_reimbursement_payable_amount(self):
        debit = credit = amount = amount_currency = 0.0
        currency = self._get_currency()
        move_date = self.date_expense

        if currency:
            amount_currency = self.amount_total
            amount = currency.with_context(date=move_date).compute(
                amount_currency,
                self.company_id.currency_id,
            )
        else:
            amount = self.amount_total

        if amount < 0.0:
            debit = amount
        else:
            credit = amount
            amount_currency *= -1.0

        return debit, credit, amount_currency

    @api.multi
    def _prepare_account_move(self):
        self.ensure_one()
        period = self.env["account.period"].find(self.date_expense)[0]
        return {
            "date": self.date_expense,
            "journal_id": self.journal_id.id,
            "name": self.name,
            "period_id": period.id,
        }

    @api.multi
    def _prepare_payable_reimbursement_move_lines(self):
        self.ensure_one()
        currency = self._get_currency()
        debit, credit, amount_currency = self._get_reimbursement_payable_amount()
        move_name = _("Employee reimbursement %s" % (self.name))
        return {
            "name": move_name,
            "move_id": self.move_id.id,
            "partner_id": self._get_partner().id,
            "account_id": self.employee_reimbursement_payable_account_id.id,
            "debit": debit,
            "credit": credit,
            "currency_id": currency and currency.id or False,
            "amount_currency": amount_currency,
            "reimbursement_id": self.id,
            "date_maturity": self.date_due,
        }

    @api.multi
    def _get_partner(self):
        self.ensure_one()
        if not self.employee_id.address_home_id:
            err_msg = _("No home address defined for employee")
            raise UserError(err_msg)
        return self.employee_id.address_home_id

    @api.onchange(
        "type_id",
    )
    def onchange_journal_id(self):
        self.journal_id = False
        if self.type_id:
            self.journal_id = self.type_id.journal_id

    @api.onchange(
        "employee_id",
    )
    def onchange_department_id(self):
        self.department_id = False
        if self.employee_id:
            self.department_id = self.employee_id.department_id

    @api.onchange(
        "employee_id",
    )
    def onchange_manager_id(self):
        self.manager_id = False
        if self.employee_id:
            self.manager_id = self.employee_id.parent_id

    @api.onchange(
        "employee_id",
    )
    def onchange_job_id(self):
        self.job_id = False
        if self.employee_id:
            self.job_id = self.employee_id.job_id

    @api.onchange(
        "type_id",
        "employee_id",
    )
    def onchange_employee_reimbursement_payable_account_id(self):
        result = False
        if self.employee_id:
            result = self.employee_id.employee_reimbursement_payable_account_id

        if not result and self.type_id:
            result = self.type_id.employee_reimbursement_payable_account_id

        self.employee_reimbursement_payable_account_id = result

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for document in self:
            if document.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(HrReimbursement, self)
        _super.unlink()

    @api.multi
    def validate_tier(self):
        _super = super(HrReimbursement, self)
        _super.validate_tier()
        for document in self:
            if document.validated:
                document.action_approve()

    @api.multi
    def restart_validation(self):
        _super = super(HrReimbursement, self)
        _super.restart_validation()
        for document in self:
            document.request_validation()

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
