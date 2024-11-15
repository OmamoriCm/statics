# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ServiceQuotationFixItem(models.AbstractModel):
    _name = "service.common_fix_item"
    _description = "Service Common Fix Item"
    _auto = False
    _order = "id desc"

    contract_id = fields.Many2one(
        string="# Contract",
        comodel_name="service.contract_common",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    name = fields.Char(
        string="Description",
        required=True,
    )
    price_unit = fields.Float(
        string="Price Unit",
    )
    quantity = fields.Float(
        string="Qty",
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
    )
    amount_untaxed = fields.Float(
        string="Untaxed",
    )
    amount_tax = fields.Float(
        string="Tax",
    )
    amount_total = fields.Float(
        string="Total",
    )
