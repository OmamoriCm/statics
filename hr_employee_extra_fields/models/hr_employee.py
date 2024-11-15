# -*- coding: utf-8 -*-
from openerp import fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    din = fields.Char(size=35, string='CIN')
    tin = fields.Char(size=35, string='RUC')
    sin = fields.Char(size=35, string='IPS')
    ein = fields.Char(size=35, string='EIN')
