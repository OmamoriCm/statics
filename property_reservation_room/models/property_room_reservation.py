# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class PropertyRoomReservation(models.Model):
    _inherit = "property.reservation_common"
    _name = "property.room_reservation"
    _description = "Room Reservation"

    @api.model
    def _default_type_id(self):
        return self.env.ref(
            "property_reservation_room.reservation_type_room").id

    type_id = fields.Many2one(
        default=lambda self: self._default_type_id(),
    )
    property_id = fields.Many2one(
        string="Room",
        comodel_name="property.room",
        required=True,
    )
