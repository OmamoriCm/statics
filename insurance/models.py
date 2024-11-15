# -*- coding: utf-8 -*-

from openerp import models, fields, api



class insurance(models.Model):
    _name = 'hr.contract'
    _inherit = 'hr.contract'



    insurance_number=fields.Char(String='Insurance number')
    insurance_company= fields.Many2one('hr.employee', "Insurance company", readonly=False)
    insurance_amount=fields.Float("Insurance employee amount%", readonly=False)
    insurance_percentage=fields.Float("insurance company persentage%",readonly=False)
    insurance_medical=fields.Float("insurance medical amount",readonly=False)

















