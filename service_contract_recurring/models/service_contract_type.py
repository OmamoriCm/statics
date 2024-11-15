# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ServiceContractType(models.Model):
    _name = "service.contract_type"
    _inherit = "service.contract_type"

    recurring_item_allowed_product_ids = fields.Many2many(
        string="Recurring Item Allowed Products",
        comodel_name="product.product",
        relation="rel_contract_type_2_recurring_item_allowed_product",
        column1="type_id",
        column2="product_id",
    )
    recurring_item_allowed_product_categ_ids = fields.Many2many(
        string="Recurring Item Allowed Product Categories",
        comodel_name="product.category",
        relation="rel_contract_type_2_recurring_item_allowed_product_categ",
        column1="type_id",
        column2="product_id",
    )
    recurring_item_receivable_journal_id = fields.Many2one(
        string="Recurring Item Receivable Journal",
        comodel_name="account.journal",
        company_dependent=True,
    )
    recurring_item_receivable_account_id = fields.Many2one(
        string="Recurring Item Receivable Account",
        comodel_name="account.account",
        company_dependent=True,
    )
    recurring_service_ok = fields.Boolean(
        string="Recurring Service?",
        default=False,
    )
