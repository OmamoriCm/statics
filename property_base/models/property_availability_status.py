# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class PropertyAvailabilityStatus(models.Model):
    _name = "property.availability_status"
    _description = "Availability Status"

    name = fields.Char(
        string="Availability Status",
        required=True,
    )
    note = fields.Text(
        string="Notes"
    )
    active = fields.Boolean(
        string="Active",
        default=True
    )
