from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime


class tci_company(models.Model):

    _inherit = "res.company"
    
    acn_number = fields.Char(string="ACN")
    abn_number = fields.Char(string="ABN")