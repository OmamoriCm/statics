# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ServiceContractTeam(models.Model):
    _name = "service.contract_team"
    _description = "Service Contract Team"

    contract_id = fields.Many2one(
        string="# Contract",
        comodel_name="service.contract",
        required=True,
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        string="Function",
        comodel_name="product.product",
        required=True,
    )
    user_id = fields.Many2one(
        string="Team",
        comodel_name="res.users",
        required=True,
    )
