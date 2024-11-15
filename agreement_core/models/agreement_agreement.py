# -*- coding: utf-8 -*-
# Copyright 2018-2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class AgreementAgreement(models.Model):
    _name = "agreement.agreement"
    _description = "Agreement"
    _order = "date_agreement desc, id desc"
    _inherit = [
        "agreement.abstract",
        "mail.thread",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.document_version",
        "base.cancel.reason_common",
    ]

    @api.model
    def _default_user_id(self):
        return self.env.user.id

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id

    @api.multi
    @api.depends(
        "company_id",
    )
    def _compute_policy(self):
        _super = super(AgreementAgreement, self)
        _super._compute_policy()

    name = fields.Char(
        string="# Agreement",
        required=True,
        default="/",
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    signed_document_id = fields.Many2one(
        string="Signed Document",
        comodel_name="ir.attachment",
        readonly=True,
        ondelete="restrict",
    )
    type_id = fields.Many2one(
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    title = fields.Char(
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    raw_description = fields.Text(
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
    date_agreement = fields.Date(
        string="Date Agreement",
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
    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        default=lambda self: self._default_user_id(),
        select=True,
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    parent_id = fields.Many2one(
        string="Parent Agreement",
        comodel_name="agreement.agreement",
        select=True,
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
        domain=[
            ("parent_id", "=", False),
        ],
        select=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    template_id = fields.Many2one(
        string="Template",
        comodel_name="agreement.template",
        select=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    section_ids = fields.One2many(
        comodel_name="agreement.agreement_section",
        inverse_name="agreement_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    party_ids = fields.One2many(
        comodel_name="agreement.agreement_party",
        inverse_name="agreement_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    recital_ids = fields.One2many(
        comodel_name="agreement.agreement_recital",
        inverse_name="agreement_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    appendix_ids = fields.One2many(
        comodel_name="agreement.agreement_appendix",
        inverse_name="agreement_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    state = fields.Selection(
        string="State",
        copy=False,
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("approve", "Approved"),
            ("active", "Active"),
            ("expire", "Expired"),
            ("terminate", "Terminated"),
            ("cancel", "Cancelled"),
        ],
        required=True,
        readonly=True,
        default="draft",
    )
    terminate_reason_id = fields.Many2one(
        string="Terminate Reason",
        comodel_name="agreement.termination_reason",
        readonly=True,
    )
    previous_version_id = fields.Many2one(
        comodel_name="agreement.agreement",
    )
    origin_version_id = fields.Many2one(
        comodel_name="agreement.agreement",
    )

    # Log Fields
    confirmed_date = fields.Datetime(
        string="Confirmation Date",
        readonly=True,
        copy=False,
    )
    confirmed_user_id = fields.Many2one(
        string="Confirmation By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    approved_date = fields.Datetime(
        string="Approved Date",
        readonly=True,
        copy=False,
    )
    approved_user_id = fields.Many2one(
        string="Approved By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    active_date = fields.Datetime(
        string="Active Date",
        readonly=True,
        copy=False,
    )
    active_user_id = fields.Many2one(
        string="Activated By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    expire_date = fields.Datetime(
        string="Expired Date",
        readonly=True,
        copy=False,
    )
    expire_user_id = fields.Many2one(
        string="Expired By",
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
    cancelled_date = fields.Datetime(
        string="Cancellation Date",
        readonly=True,
        copy=False,
    )
    cancelled_user_id = fields.Many2one(
        string="Cancellation By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    # Policy Fields
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    print_ok = fields.Boolean(
        string="Can Print",
        compute="_compute_policy",
    )
    attach_ok = fields.Boolean(
        string="Can Attach Signed Document",
        compute="_compute_policy",
    )
    approve_ok = fields.Boolean(
        string="Can Approve",
        compute="_compute_policy",
    )
    active_ok = fields.Boolean(
        string="Can Activate",
        compute="_compute_policy",
    )
    expire_ok = fields.Boolean(
        string="Can Set as Expire",
        compute="_compute_policy",
    )
    terminate_ok = fields.Boolean(
        string="Can Terminate",
        compute="_compute_policy",
    )
    revision_ok = fields.Boolean(
        string="Can Create Revision",
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

    @api.multi
    def onchange_template_id(self, template_id):
        value = {
            "title": "",
            "type_id": False,
            "raw_description": "",
            "recital_ids": [],
            "section_ids": [],
            "appendix_ids": [],
            "party_ids": [],
        }
        domain = {}
        obj_template = self.env["agreement.template"]
        if template_id:
            template = obj_template.browse([template_id])[0]
            value["title"] = template.title
            value["type_id"] = template.type_id.id
            value["raw_description"] = template.raw_description
            value["recital_ids"] = template._prepare_recital()
            value["section_ids"] = template._prepare_section()
            value["appendix_ids"] = template._prepare_appendix()
            value["party_ids"] = template._prepare_party()
            value["report_id"] = template.report_id and template.report_id.id or False
        return {"value": value, "domain": domain}

    @api.model
    def create(self, values):
        _super = super(AgreementAgreement, self)
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
        for agreement in self:
            if agreement.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(AgreementAgreement, self)
        _super.unlink()

    @api.multi
    def button_confirm(self):
        for agreement in self:
            agreement.write(agreement._prepare_confirm_data())

    @api.multi
    def button_approve(self):
        for agreement in self:
            agreement.write(agreement._prepare_approve_data())

    @api.multi
    def button_active(self):
        for agreement in self:
            agreement.write(agreement._prepare_active_data())

    @api.multi
    def button_print(self):
        for agreement in self:
            if agreement.report_id:
                return agreement.report_id.read()[0]
            else:
                msg = _("No report template defined")
                raise UserError(msg)

    @api.multi
    def button_expire(self):
        for agreement in self:
            agreement.write(agreement._prepare_expire_data())

    @api.multi
    def button_terminate(self, terminate_reason_id=False):
        for agreement in self:
            agreement.write(agreement._prepare_terminate_data(terminate_reason_id))

    @api.multi
    def button_cancel(self, cancel_reason_id=False):
        for agreement in self:
            attachment = agreement.signed_document_id
            agreement.write(agreement._prepare_cancel_data(cancel_reason_id))
            if attachment:
                attachment.unlink()

    @api.multi
    def button_restart(self):
        for agreement in self:
            if agreement._allow_to_restart():
                agreement.write(agreement._prepare_restart_data())
            else:
                msg = _("You can not restart agreement with revisions")
                raise UserError(msg)

    @api.model
    def _prepare_confirm_data(self):
        result = {
            "state": "confirm",
            "confirmed_date": fields.Datetime.now(),
            "confirmed_user_id": self.env.user.id,
        }
        return result

    @api.model
    def _prepare_approve_data(self):
        result = {
            "state": "approve",
            "approved_date": fields.Datetime.now(),
            "approved_user_id": self.env.user.id,
        }
        return result

    @api.model
    def _prepare_active_data(self):
        result = {
            "state": "active",
            "active_date": fields.Datetime.now(),
            "active_user_id": self.env.user.id,
        }
        return result

    @api.model
    def _prepare_expire_data(self):
        result = {
            "state": "expire",
            "expire_date": fields.Datetime.now(),
            "expire_user_id": self.env.user.id,
        }
        return result

    @api.model
    def _prepare_cancel_data(self, cancel_reason_id=False):
        result = {
            "state": "cancel",
            "cancelled_date": fields.Datetime.now(),
            "cancelled_user_id": self.env.user.id,
            "cancel_reason_id": cancel_reason_id,
            "signed_document_id": False,
        }
        return result

    @api.model
    def _prepare_terminate_data(self, terminate_reason_id=False):
        result = {
            "state": "terminate",
            "terminate_date": fields.Datetime.now(),
            "terminate_user_id": self.env.user.id,
            "terminate_reason_id": terminate_reason_id,
        }
        return result

    @api.model
    def _prepare_restart_data(self):
        result = {
            "state": "draft",
            "confirmed_date": False,
            "confirmed_user_id": False,
            "approved_date": False,
            "approved_user_id": False,
            "active_date": False,
            "active_user_id": False,
            "expire_date": False,
            "expire_user_id": False,
            "terminate_date": False,
            "terminate_user_id": False,
            "terminate_reason_id": False,
            "cancelled_date": False,
            "cancelled_user_id": False,
            "cancel_reason_id": False,
        }
        return result

    @api.multi
    def _allow_to_restart(self):
        self.ensure_one()
        if self.total_revision > 0:
            return False
        else:
            return True

    @api.constrains("state")
    def _constrain_only_one_version(self):
        obj_agreement = self.env["agreement.agreement"]
        for agreement in self:
            if agreement.state == "active":
                criteria = [
                    ("id", "!=", agreement.id),
                    ("state", "=", "active"),
                ]
                if agreement.origin_version_id:
                    origin = agreement.origin_version_id
                    criteria += [
                        "|",
                        ("origin_version_id", "=", origin.id),
                        ("id", "=", origin.id),
                    ]
                else:
                    criteria += [
                        ("origin_version_id", "=", agreement.id),
                    ]
                if obj_agreement.search_count(criteria) > 0:
                    msg = _("There is already active agreement")
                    raise UserError(msg)

    @api.constrains(
        "state",
    )
    def _constrains_signed_doc(self):
        for agreement in self:
            if agreement.state == "approve" and not agreement.signed_document_id:
                msg = _("Please attach signed document")
                raise UserError(msg)
