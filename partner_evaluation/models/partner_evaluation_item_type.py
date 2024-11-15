# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.safe_eval import safe_eval as eval


class PartnerEvaluationItemType(models.Model):
    _name = "partner.evaluation_item_type"
    _description = "Partner Evaluation Item Type"

    name = fields.Char(
        string="Evaluation Item Type",
        required=True,
    )
    code = fields.Char(
        string="Code",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    method = fields.Selection(
        string="Method",
        selection=[
            ("manual", "Manual"),
            ("automatic", "Automatic"),
        ],
        required=True,
        default="manual",
    )
    python_code = fields.Text(
        string="Python Code",
    )
    question_type = fields.Selection(
        string="Type",
        selection=[
            ("qualitative", "Qualitative"),
            ("quantitative", "Quantitative"),
        ],
        required=True,
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
    )
    qualitative_option_ids = fields.One2many(
        string="Qualitative Options",
        comodel_name="partner.evaluation_item_type_qualitative_option",
        inverse_name="type_id",
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
        if self.question_type == "qualitative":
            result = False
        else:
            result = 0.0

        localdict = self._get_localdict(document)

        try:
            eval(self.python_code, localdict, mode="exec", nocopy=True)
            result = localdict["result"]
        except:  # noqa: E722
            raise UserError(_("Error on computation"))

        return result
