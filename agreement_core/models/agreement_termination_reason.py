# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AgreementTerminationReason(models.Model):
    _name = "agreement.termination_reason"
    _description = "Agreement Termination Reason"

    name = fields.Char(
        string="Termination Reason",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
