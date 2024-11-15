# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class CrmMakeSale(models.TransientModel):
    _inherit = "crm.make.sale"

    sale_id = fields.Many2one(
        string="Quotation/Sale Order",
        comodel_name="sale.order",
    )

    @api.multi
    def makeOrder(self):
        self.ensure_one()
        _super = super(CrmMakeSale, self)
        obj_case = self.env["crm.lead"]
        case = obj_case.browse([self.env.context.get("active_id", False)])[0]
        if case.sale_id:
            msg = _("Quotation/Sale Order already exist")
            raise UserError(msg)
        result = _super.makeOrder()
        sale_id = result["res_id"]
        case.write({"sale_id": sale_id})
        case.sale_id.write({"case_id": case.id})
        return result
