# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields


class Website(models.Model):
    _inherit = 'website'

    edit_portal_addresses = fields.Boolean(
        string='Edit portal addresses',
        help='Allow to create and edit addresses in customers portal',
        default=True)
