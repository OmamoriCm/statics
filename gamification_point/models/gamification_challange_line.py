# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class GamificationChallangeLine(models.Model):
    _inherit = "gamification.challenge.line"

    reach_point = fields.Float(
        string="Point Assigned When Goal Reached",
        required=True,
        default=0.0,
    )
    fail_point = fields.Float(
        string="Point Assigned When Goal Failed",
        required=True,
        default=0.0,
    )
    reach_point_method = fields.Selection(
        string="Reached Point Method",
        selection=[("fixed", "Fixed"), ("multiply", "Multiply Current Result")],
        default="fixed",
        required=True,
    )
    fail_point_method = fields.Selection(
        string="Failed Point Method",
        selection=[("fixed", "Fixed"), ("multiply", "Multiply Current Result")],
        default="fixed",
        required=True,
    )
