# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ServiceContractType(models.Model):
    _name = "service.contract_type"
    _inherit = "service.contract_type"

    man_hour_allowed_product_ids = fields.Many2many(
        string="Man Hour Allowed Products",
        comodel_name="product.product",
        relation="rel_contract_type_2_man_hour_allowed_product",
        column1="type_id",
        column2="product_id",
    )
    man_hour_allowed_product_categ_ids = fields.Many2many(
        string="Man Hour Allowed Product Categories",
        comodel_name="product.category",
        relation="rel_contract_type_2_man_hour_allowed_product_categ",
        column1="type_id",
        column2="product_id",
    )
    man_hour_receivable_journal_id = fields.Many2one(
        string="Man Hour Receivable Journal",
        comodel_name="account.journal",
        company_dependent=True,
    )
    man_hour_receivable_account_id = fields.Many2one(
        string="Man Hour Receivable Account",
        comodel_name="account.account",
        company_dependent=True,
    )
    man_hour_ok = fields.Boolean(
        string="Man Hour?",
        default=False,
    )
