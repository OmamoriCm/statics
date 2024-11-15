# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    is_psychology_client = fields.Boolean(
        string="Is Psychology Client",
        default=False,
    )
