# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.safe_eval import safe_eval as eval


class PartnerEvaluationTemplate(models.Model):
    _name = "partner.evaluation_template"
    _description = "Partner Evaluation Template"

    name = fields.Char(
        string="Evaluation Template",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    require_duration = fields.Boolean(
        string="Require Duration",
        default=False,
    )
    item_ids = fields.One2many(
        string="Items",
        comodel_name="partner.evaluation_template_item",
        inverse_name="template_id",
    )
    manual_result = fields.Boolean(
        string="Manual Result",
        default=False,
    )
    python_code_result = fields.Text(
        string="Python Code for Automatic Result Computation",
    )
    result_ids = fields.One2many(
        string="Results",
        comodel_name="partner.evaluation_result",
        inverse_name="template_id",
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
    )
    note = fields.Text(
        string="Note",
    )
    partner_evaluation_confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm Partner Evaluation",
        comodel_name="res.groups",
        relation="rel_template_2_confirm_partner_evaluation",
        column1="type_id",
        column2="group_id",
    )
    partner_evaluation_approve_grp_ids = fields.Many2many(
        string="Allow To Approve Partner Evaluation",
        comodel_name="res.groups",
        relation="rel_template_2_approve_partner_evaluation",
        column1="type_id",
        column2="group_id",
    )
    partner_evaluation_start_grp_ids = fields.Many2many(
        string="Allow To Confirm Partner Evaluation",
        comodel_name="res.groups",
        relation="rel_template_2_start_partner_evaluation",
        column1="type_id",
        column2="group_id",
    )
    partner_evaluation_done_grp_ids = fields.Many2many(
        string="Allow To Finish Partner Evaluation",
        comodel_name="res.groups",
        relation="rel_template_2_done_partner_evaluation",
        column1="type_id",
        column2="group_id",
    )
    partner_evaluation_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel Partner Evaluation",
        comodel_name="res.groups",
        relation="rel_template_2_cancel_partner_evaluation",
        column1="type_id",
        column2="group_id",
    )
    partner_evaluation_restart_grp_ids = fields.Many2many(
        string="Allow To Restart Partner Evaluation",
        comodel_name="res.groups",
        relation="rel_template_2_restart_partner_evaluation",
        column1="type_id",
        column2="group_id",
    )
    note = fields.Text(
        string="Note",
    )

    def _get_localdict(self, document):
        self.ensure_one()
        return {
            "env": self.env,
            "document": document,
        }

    @api.multi
    def _get_result(self, document):
        self.ensure_one()
        result = False
        localdict = self._get_localdict(document)

        try:
            eval(self.python_code_result, localdict, mode="exec", nocopy=True)
            result = localdict["result"]
        except:  # noqa: E722
            raise UserError(_("Error on computation"))

        return result
