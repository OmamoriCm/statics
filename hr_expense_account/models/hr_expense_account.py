# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class HrExpenseAccount(models.Model):
    _name = "hr.expense_account"
    _description = "Employee Expense Account"
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

    @api.multi
    def _compute_policy(self):
        _super = super(HrExpenseAccount, self)
        _super._compute_policy()

    @api.depends(
        "amount_limit",
    )
    def _compute_amount(self):
        for record in self:
            amount_realize = amount_residual = 0.0
            amount_residual = record.amount_limit - amount_realize
            record.amount_realize = amount_realize
            record.amount_residual = amount_residual

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
    type_id = fields.Many2one(
        string="Type",
        comodel_name="hr.expense_account_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    amount_limit = fields.Float(
        string="Amount Limit",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    amount_realize = fields.Float(
        string="Amount Realize",
        compute="_compute_amount",
        store=True,
    )
    amount_residual = fields.Float(
        string="Amount Residual",
        compute="_compute_amount",
        store=True,
    )
    date_assign = fields.Date(
        string="Date Assign",
        default=lambda self: fields.Date.today(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_expire = fields.Date(
        string="Date Expire",
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
            ("approve", "Open"),
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
        for document in self:
            document._run_pre_confirm_check()
            document.write(document._prepare_confirm_data())
            document.request_validation()
            document._run_post_confirm_check()

    @api.multi
    def _run_pre_confirm_check(self):
        self.ensure_one()
        method_names = [
            method_name
            for method_name in dir(self)
            if method_name.startswith("_pre_confirm_check")
        ]
        for method_name in method_names:
            getattr(self, method_name)()

    @api.multi
    def _run_post_confirm_check(self):
        self.ensure_one()
        method_names = [
            method_name
            for method_name in dir(self)
            if method_name.startswith("_post_confirm_check")
        ]
        for method_name in method_names:
            getattr(self, method_name)()

    @api.multi
    def action_approve(self):
        for document in self:
            document._run_pre_approve_check()
            document.write(document._prepare_approve_data())
            document._run_post_approve_check()

    @api.multi
    def _run_pre_approve_check(self):
        self.ensure_one()
        method_names = [
            method_name
            for method_name in dir(self)
            if method_name.startswith("_pre_approve_check")
        ]
        for method_name in method_names:
            getattr(self, method_name)()

    @api.multi
    def _run_post_approve_check(self):
        self.ensure_one()
        method_names = [
            method_name
            for method_name in dir(self)
            if method_name.startswith("_post_approve_check")
        ]
        for method_name in method_names:
            getattr(self, method_name)()

    @api.multi
    def action_done(self):
        for document in self:
            document._run_pre_done_check()
            document.write(document._prepare_done_data())
            document._run_post_done_check()

    @api.multi
    def _run_pre_done_check(self):
        self.ensure_one()
        method_names = [
            method_name
            for method_name in dir(self)
            if method_name.startswith("_pre_done_check")
        ]
        for method_name in method_names:
            getattr(self, method_name)()

    @api.multi
    def _run_post_done_check(self):
        self.ensure_one()
        method_names = [
            method_name
            for method_name in dir(self)
            if method_name.startswith("_post_done_check")
        ]
        for method_name in method_names:
            getattr(self, method_name)()

    @api.multi
    def action_terminate(self):
        for document in self:
            document._run_pre_terminate_check()
            document.write(document._prepare_terminate_data())
            document._run_post_terminate_check()

    @api.multi
    def _run_pre_terminate_check(self):
        self.ensure_one()
        method_names = [
            method_name
            for method_name in dir(self)
            if method_name.startswith("_pre_terminate_check")
        ]
        for method_name in method_names:
            getattr(self, method_name)()

    @api.multi
    def _run_post_terminate_check(self):
        self.ensure_one()
        method_names = [
            method_name
            for method_name in dir(self)
            if method_name.startswith("_post_terminate_check")
        ]
        for method_name in method_names:
            getattr(self, method_name)()

    @api.multi
    def action_cancel(self):
        for document in self:
            document._run_pre_cancel_check()
            document.write(document._prepare_cancel_data())
            document.restart_validation()
            document._run_post_cancel_check()

    @api.multi
    def _run_pre_cancel_check(self):
        self.ensure_one()
        method_names = [
            method_name
            for method_name in dir(self)
            if method_name.startswith("_pre_cancel_check")
        ]
        for method_name in method_names:
            getattr(self, method_name)()

    @api.multi
    def _run_post_cancel_check(self):
        self.ensure_one()
        method_names = [
            method_name
            for method_name in dir(self)
            if method_name.startswith("_post_cancel_check")
        ]
        for method_name in method_names:
            getattr(self, method_name)()

    @api.multi
    def action_restart(self):
        for document in self:
            document._run_pre_restart_check()
            document.write(document._prepare_restart_data())
            document._run_post_restart_check()

    @api.multi
    def _run_pre_restart_check(self):
        self.ensure_one()
        method_names = [
            method_name
            for method_name in dir(self)
            if method_name.startswith("_pre_restart_check")
        ]
        for method_name in method_names:
            getattr(self, method_name)()

    @api.multi
    def _run_post_restart_check(self):
        self.ensure_one()
        method_names = [
            method_name
            for method_name in dir(self)
            if method_name.startswith("_post_restart_check")
        ]
        for method_name in method_names:
            getattr(self, method_name)()

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
                "ir_sequence_date": self.date_assign,
            }
        )
        sequence = self.with_context(ctx)._create_sequence()
        return {
            "state": "approve",
            "name": sequence,
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

    @api.multi
    def unlink(self):
        strWarning1 = _("You can only delete data on draft state")
        strWarning2 = _("You can not delete data with document number")
        for document in self:
            if document.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning1)
            if document.name != "/":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning2)
        _super = super(HrExpenseAccount, self)
        _super.unlink()

    @api.multi
    def validate_tier(self):
        _super = super(HrExpenseAccount, self)
        _super.validate_tier()
        for document in self:
            if document.validated:
                document.action_approve()

    @api.multi
    def restart_validation(self):
        _super = super(HrExpenseAccount, self)
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
