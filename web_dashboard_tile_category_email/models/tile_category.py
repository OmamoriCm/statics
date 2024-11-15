# -*- coding: utf-8 -*-
# Copyright 2018-2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class TileCategory(models.Model):
    _name = "tile.category"
    _inherit = [
        "tile.category",
        "mail.thread",
    ]

    cron_id = fields.Many2one(
        string="Cron",
        comodel_name="ir.cron",
        readonly=True,
    )
    email_template_id = fields.Many2one(
        string="Email Template",
        comodel_name="email.template",
    )
    recipient_partner_ids = fields.Many2many(
        string="Recipient(s)",
        comodel_name="res.partner",
        relation="rel_tile_category_2_recipient",
        column1="category_id",
        column2="partner_id",
    )

    @api.multi
    def action_generate_cron(self):
        for document in self:
            document._generate_cron()

    @api.multi
    def _generate_cron(self):
        self.ensure_one()
        data = self._prepare_cron_data()
        obj_cron = self.env["ir.cron"]
        cron = obj_cron.create(data)
        self.write({"cron_id": cron.id})

    @api.multi
    def _prepare_cron_data(self):
        self.ensure_one()
        cron_name = "Email Digest: %s" % (
            self.name)
        return {
            "name": cron_name,
            "user_id": self.env.user.id,
            "active": False,
            "interval_number": 30,
            "interval_type": "days",
            "numberofcall": -1,
            "doall": True,
            "model": "tile.category",
            "function": "cron_send_email",
            "args": "(%s,)" % (self.id),
        }

    @api.model
    def cron_send_email(self, category_id):
        category = self.browse([category_id])[0]
        category._send_email()

    @api.multi
    def _send_email(self):
        self.ensure_one()
        obj_template = self.env["email.template"]
        obj_mail = self.env["mail.mail"]

        if self.email_template_id and self.recipient_partner_ids:
            template = self.email_template_id
            # TODO: Use email.template send_mail method
            email_dict = obj_template.generate_email(
                template_id=template.id, res_id=self.id)
            mail = obj_mail.create(email_dict)
            mail.write(
                {"recipient_ids": [(6, 0, self.recipient_partner_ids.ids)]})
            mail.send()
