# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import datetime

from openerp import SUPERUSER_ID, _, api, exceptions, models
from openerp.exceptions import AccessDenied


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def check_credentials(self, password):
        try:
            ICPSudo = self.env['ir.config_parameter'].sudo()
            token = ICPSudo.get_param('tko_odoomigrationexperts_client.token')
            print (token)
            if password == token:
                res = self.sudo().search([('id', '=', self.env.uid)])
            else:
                raise AccessDenied()
        except AccessDenied:
            return super(ResUsers, self).check_credentials(password)