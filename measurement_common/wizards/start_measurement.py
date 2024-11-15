# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class StartMeasurement(models.TransientModel):
    _name = "measurement.start_measurement"
    _description = "Start Measurement"

    @api.model
    def _default_date_start(self):
        return fields.Datetime.now()

    date_start = fields.Datetime(
        string="Date Start",
        required=True,
        default=lambda self: self._default_date_start(),
    )

    @api.multi
    def action_start(self):
        self.ensure_one()
        object_name = self._context.get("active_model", False)
        obj_measurement = self.env[object_name]
        object_ids = self._context.get("active_ids", [])
        for measurement_object in obj_measurement.browse(object_ids):
            measurement_object.write(
                measurement_object._prepare_start_data(self.date_start))
