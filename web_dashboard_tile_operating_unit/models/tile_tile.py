# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class TileTile(models.Model):
    _inherit = "tile.tile"

    operating_unit_ids = fields.Many2many(
        string="Operating Unit",
        comodel_name="operating.unit",
        relation="rel_tile_2_operating_unit",
        column1="tile_id",
        column2="operating_unit",
    )
