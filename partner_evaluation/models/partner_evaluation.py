# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class PartnerEvaluation(models.Model):
    _name = "partner.evaluation"
    _inherit = [
        "mail.thread",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
    ]
    _description = "Partner Evaluation"

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.model
    def _default_user_id(self):
        return self.env.user.id

    @api.multi
    @api.depends(
        "template_id",
    )
    def _compute_policy(self):
        _super = super(PartnerEvaluation, self)
        _super._compute_policy()

    @api.multi
    @api.depends(
        "template_id",
    )
    def _compute_require_duration(self):
        for document in self:
            document.require_duration = document.template_id.require_duration

    name = fields.Char(
        string="# Document",
        default="/",
        help="""Document number

Leave / to assign automatic document number.
Automatic document number will be assign when data created.
Change / to assign document number manually.
        """,
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
    template_id = fields.Many2one(
        string="Template",
        comodel_name="partner.evaluation_template",
        required=True,
        help="Template",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
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
    date_start = fields.Date(
        string="Date Start",
        help="Evaluation period start date",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_end = fields.Date(
        string="Date End",
        help="Evaluation period end date",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    scheduled_date_start = fields.Datetime(
        string="Evaluation Scheduled Date Start",
        required=True,
        help="Evaluation schedule date start",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    scheduled_date_end = fields.Datetime(
        string="Evaluation Date End",
        required=True,
        help="Evaluation schedule date end",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    real_date_start = fields.Datetime(
        string="Real Date Start",
        help="Evaluation real date start",
        readonly=True,
    )
    real_date_end = fields.Datetime(
        string="Real Date End",
        help="Evaluation real date start",
        readonly=True,
    )
    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        default=lambda self: self._default_user_id(),
        help="Person who responsible to evaluate",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    item_ids = fields.One2many(
        string="Items",
        comodel_name="partner.evaluation_item",
        inverse_name="evaluation_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    result_id = fields.Many2one(
        string="Result",
        comodel_name="partner.evaluation_result",
        readonly=True,
    )
    require_duration = fields.Boolean(
        string="Require Duration",
        compute="_compute_require_duration",
        store=False,
    )
    note = fields.Text(
        string="Note",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("approve", "Ready To Start"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        required=True,
        readonly=True,
    )
    # Policy Field
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    approve_ok = fields.Boolean(
        string="Can Approve",
        compute="_compute_policy",
    )
    start_ok = fields.Boolean(
        string="Can Start",
        compute="_compute_policy",
    )
    done_ok = fields.Boolean(
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
    # Log Fields
    confirm_date = fields.Datetime(
        string="Confirm Date",
        readonly=True,
    )
    confirm_user_id = fields.Many2one(
        string="Confirmed By",
        comodel_name="res.users",
        readonly=True,
    )
    approve_date = fields.Datetime(
        string="Approve Date",
        readonly=True,
    )
    approve_user_id = fields.Many2one(
        string="Approve By",
        comodel_name="res.users",
        readonly=True,
    )
    start_user_id = fields.Many2one(
        string="Start By",
        comodel_name="res.users",
        readonly=True,
    )
    start_date = fields.Datetime(
        string="Start Date",
        readonly=True,
    )
    done_date = fields.Datetime(
        string="Finish Date",
        readonly=True,
    )
    done_user_id = fields.Many2one(
        string="Finished By",
        comodel_name="res.users",
        readonly=True,
    )
    cancel_date = fields.Datetime(
        string="Cancel Date",
        readonly=True,
    )
    cancel_user_id = fields.Many2one(
        string="Cancelled By",
        comodel_name="res.users",
        readonly=True,
    )

    @api.constrains("scheduled_date_start", "scheduled_date_end")
    def _check_scheduled_date(self):
        strWarning = _("Scheduled date end must be " "greater than scheduled date end")
        if self.scheduled_date_start and self.scheduled_date_end:
            if self.scheduled_date_start >= self.scheduled_date_end:
                raise UserError(strWarning)

    @api.constrains("real_date_start", "real_date_end")
    def _check_real_date(self):
        strWarning = _("Real date end must be " "greater than real date end")
        if self.real_date_start and self.real_date_end:
            if self.real_date_start >= self.real_date_end:
                raise UserError(strWarning)

    @api.multi
    def action_confirm(self):
        for document in self:
            document.write(document._prepare_confirm_data())

    @api.multi
    def action_approve(self):
        for document in self:
            document.write(document._prepare_approve_data())

    @api.multi
    def action_start(self, date_start=False):
        for document in self:
            document.write(document._prepare_start_data(date_start=date_start))

    @api.multi
    def action_done(self, result=False, date_end=False):
        for document in self:
            document._compute_automatic_field()
            document.write(
                document._prepare_done_data(result=result, date_end=date_end)
            )
            document._run_server_action()

    @api.multi
    def action_cancel(self):
        for document in self:
            document.write(document._prepare_cancel_data())

    @api.multi
    def action_restart(self):
        for document in self:
            document.item_ids.unlink()
            document.write(document._prepare_restart_data())

    @api.multi
    def action_compute(self):
        for document in self:
            document._compute_automatic_field()

    @api.multi
    def _compute_automatic_field(self):
        self.ensure_one()
        for measurement_item in self.item_ids.filtered(
            lambda r: r.method == "automatic"
        ):
            measurement_item._compute_automatic_field()

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
            "state": "approve",
            "approve_date": fields.Datetime.now(),
            "approve_user_id": self.env.user.id,
            "item_ids": self._prepare_evaluation_items(),
        }

    @api.multi
    def _prepare_start_data(self, date_start=False):
        self.ensure_one()
        real_date_start = date_start or fields.Datetime.now()
        return {
            "state": "open",
            "start_date": fields.Datetime.now(),
            "start_user_id": self.env.user.id,
            "real_date_start": real_date_start,
        }

    @api.multi
    def _prepare_done_data(self, result=False, date_end=False):
        self.ensure_one()
        real_date_end = date_end or fields.Datetime.now()
        result_id = (result and result.id or False,)
        return {
            "state": "done",
            "result_id": result_id,
            "done_date": fields.Datetime.now(),
            "done_user_id": self.env.user.id,
            "real_date_end": real_date_end,
        }

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
            "cancel_date": fields.Datetime.now(),
            "cancel_user_id": self.env.user.id,
            "real_date_start": False,
            "real_date_end": False,
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
            "start_date": False,
            "start_user_id": False,
            "done_date": False,
            "done_user_id": False,
            "cancel_date": False,
            "cancel_user_id": False,
            "result_id": False,
        }

    @api.multi
    def _prepare_evaluation_items(self):
        self.ensure_one()
        result = []
        for item in self.template_id.item_ids:
            result.append(
                (
                    0,
                    0,
                    {
                        "sequence": item.sequence,
                        "item_type_id": item.item_type_id.id,
                        "question_type": item.item_type_id.question_type,
                        "uom_id": item.item_type_id.uom_id
                        and item.item_type_id.uom_id.id
                        or False,
                    },
                )
            )
        return result

    @api.multi
    def _run_server_action(self):
        self.ensure_one()
        if len(self.result_id.server_action_ids) > 0:
            self.result_id.server_action_ids.run()

    @api.model
    def create(self, values):
        _super = super(PartnerEvaluation, self)
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
        for document in self:
            if document.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(PartnerEvaluation, self)
        _super.unlink()
