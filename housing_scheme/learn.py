# -*- coding: utf-8 -*-


from openerp import models, fields, api, _


class learn_learn(models.Model):
    _name = "learn.learn"
    
    
    name = fields.Char(string='Name', required=True, index=True, translate=True)
    country = fields.Many2one('country.country_learn',"Country")
    
    
class country(models.Model):

    _name = 'country.country_learn'

    code = fields.Char("Code")
    name = fields.Char("Name")