# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class EndMeasurement(models.TransientModel):
    _name = "measurement.end_measurement"
    _description = "End Measurement"

    @api.model
    def _default_date_end(self):
        return fields.Datetime.now()

    date_end = fields.Datetime(
        string="Date End",
        required=True,
        default=lambda self: self._default_date_end(),
    )

    @api.multi
    def action_end(self):
        self.ensure_one()
        object_name = self._context.get("active_model", False)
        obj_measurement = self.env[object_name]
        object_ids = self._context.get("active_ids", [])
        for measurement_object in obj_measurement.browse(object_ids):
            measurement_object.write(
                measurement_object._prepare_done_data(self.date_end))
