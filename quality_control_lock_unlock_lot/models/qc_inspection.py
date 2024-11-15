# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class QcInspection(models.Model):
    _inherit = "qc.inspection"

    @api.multi
    def action_confirm(self):
        _super = super(QcInspection, self)
        _super.action_confirm()
        for inspection in self:
            if inspection._check_auto_unlock_lot():
                inspection.lot.write(inspection._prepare_unlock_lot_data())

    @api.multi
    def action_approve(self):
        _super = super(QcInspection, self)
        _super.action_approve()
        for inspection in self:
            if inspection._check_auto_unlock_lot():
                inspection.lot.write(inspection._prepare_unlock_lot_data())

    @api.multi
    def action_todo(self):
        _super = super(QcInspection, self)
        _super.action_todo()
        for inspection in self:
            if inspection._check_auto_lock_lot():
                inspection.lot.write(inspection._prepare_lock_lot_data())

    @api.multi
    def set_test(self, trigger_line, force_fill=False):
        _super = super(QcInspection, self)
        _super.set_test(trigger_line=trigger_line, force_fill=force_fill)
        for inspection in self:
            if inspection._check_auto_lock_lot():
                inspection.lot.write(inspection._prepare_lock_lot_data())

    @api.multi
    def _check_auto_lock_lot(self):
        self.ensure_one()
        result = False
        if self.test.auto_lock_lot and self.lot:
            result = True

        return result

    @api.multi
    def _check_auto_unlock_lot(self):
        self.ensure_one()
        result = False
        if self.test.auto_unlock_lot and self.lot and self.state == "success":
            result = True

        return result

    @api.multi
    def _prepare_lock_lot_data(self):
        self.ensure_one()
        data = {
            "locked": True,
        }
        return data

    @api.multi
    def _prepare_unlock_lot_data(self):
        self.ensure_one()
        data = {
            "locked": False,
        }
        return data
