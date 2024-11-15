# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    case_id = fields.Many2one(
        string="Lead/Opportunity",
        comodel_name="crm.lead",
    )
