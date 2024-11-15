# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import api, fields, models


class HrHolidays(models.Model):
    _name = "hr.holidays"
    _inherit = [
        "hr.holidays",
        "tier.validation",
        "base.workflow_policy_object",
    ]
    _state_from = [
        "draft",
        "confirm",
    ]
    _state_to = [
        "validate",
    ]
    _cancel_state = "cancel"

    @api.model
    def _default_state(self):
        return "draft"

    @api.multi
    @api.depends(
        "employee_id",
        "type",
        "holiday_type",
    )
    def _compute_policy(self):
        _super = super(HrHolidays, self)
        _super._compute_policy()

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("validate", "Valid"),
            ("validate1", "Second Approval"),
            ("refuse", "Refused"),
            ("cancel", "Cancelled"),
        ],
        default=lambda self: self._default_state(),
    )
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
        store=False,
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
        store=False,
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
        store=False,
    )
    restart_validation_ok = fields.Boolean(
        string="Can Restart Approval",
        compute="_compute_policy",
        store=False,
    )

    @api.multi
    def validate_tier(self):
        _super = super(HrHolidays, self)
        _super.validate_tier()
        for document in self:
            if document.validated:
                document.action_validate()

    @api.multi
    def restart_validation(self):
        _super = super(HrHolidays, self)
        _super.restart_validation()
        for document in self:
            document.request_validation()

    @api.multi
    def holidays_confirm(self):
        _super = super(HrHolidays, self)
        _super.holidays_confirm()

    @api.multi
    def action_confirm(self):
        for document in self:
            document.write(document._prepare_action_confirm())
            document.request_validation()

    @api.multi
    def action_validate(self):
        for document in self:
            document.write(document._prepare_action_validate())

    @api.multi
    def action_cancel(self):
        for document in self:
            document.write(document._prepare_action_cancel())

    @api.multi
    def action_restart(self):
        for document in self:
            document.write(document._prepare_action_restart())

    @api.multi
    def action_refuse(self):
        for document in self:
            document.write(document._prepare_action_refuse())

    @api.multi
    def _prepare_action_confirm(self):
        self.ensure_one()
        return {
            "state": "confirm",
        }

    @api.multi
    def _prepare_action_validate(self):
        self.ensure_one()
        return {
            "state": "validate",
        }

    @api.multi
    def _prepare_action_cancel(self):
        self.ensure_one()
        return {
            "state": "cancel",
        }

    @api.multi
    def _prepare_action_restart(self):
        self.ensure_one()
        return {
            "state": "draft",
        }

    @api.multi
    def _prepare_action_refuse(self):
        self.ensure_one()
        return {
            "state": "refuse",
        }
