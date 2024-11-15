# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class RentalPropertyDetailSchedule(models.Model):
    _name = "rental.property_detail_schedule"
    _description = "Property Rental Detail Schedule"
    _inherit = [
        "rental.detail_schedule_common"
    ]
    _description = "Rental Property Schedule"

    @api.multi
    @api.depends(
        "detail_id.rental_id.state",
    )
    def _compute_rental_state(self):
        _super = super(RentalPropertyDetailSchedule, self)
        _super._compute_rental_state()

    @api.multi
    @api.depends(
        "manual",
        "invoice_id",
        "invoice_id.state",
    )
    def _compute_state(self):
        _super = super(RentalPropertyDetailSchedule, self)
        _super._compute_state()

    detail_id = fields.Many2one(
        string="Details",
        comodel_name="rental.property_detail",
    )
    invoice_id = fields.Many2one(
        related="invoice_line_id.invoice_id",
        store=True,
    )
    rental_id = fields.Many2one(
        related="detail_id.rental_id",
        comodel_name="rental.property",
        store=True,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        related="detail_id.rental_id.partner_id",
        store=True,
    )
    object_id = fields.Many2one(
        string="Property",
        comodel_name="property.object",
        related="detail_id.object_id",
        store=True,
    )
    state = fields.Selection(
        compute="_compute_state",
    )
