# -*- coding: utf-8 -*-
from openerp import tools, models, fields, api

class vieterp_mail_server_source(models.Model):
    _inherit = 'fetchmail.server'
    _name = 'mail.server.source'