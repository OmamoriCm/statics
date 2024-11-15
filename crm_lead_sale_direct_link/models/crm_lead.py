# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    sale_id = fields.Many2one(
        string="Quotation/Sale Order",
        comodel_name="sale.order",
    )
