# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class PropertyObject(models.Model):
    _name = "property.object"
    _inherit = [
        "rental.object",
        "property.object",
    ]
