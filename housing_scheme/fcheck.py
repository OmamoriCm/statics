# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Serpent Consulting Services Pvt. Ltd.
#    Copyright (C) 2014-2015 Serpent Consulting Services Pvt. Ltd. (<http://www.serpentcs.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp import models, fields, api

class fcheck(models.Model):
    _name = 'fcheck.model'
    
    
    name = fields.Char(string='Name')
    plot = fields.Integer(string='Plot No')
    block = fields.Selection([('a','A'),('b','B'),('c','C'),('d','D')], "Block", default="a")
    active = fields.Boolean(string='Active', default=True)
    
    flawn = fields.Float(string='Front Lawn')
    lpass = fields.Float(string='Left Passage')
    rpass = fields.Float(string='Right Passage')
    bpass = fields.Float(string='Back Passage')
    fbwall = fields.Float(string='Front Boundry Wall')
    bbwall = fields.Float(string='Back Boundry Wall')
    rbwall = fields.Float(string='Right Boundry Wall')
    lbwall = fields.Float(string='Left Boundry Wall')
    
    ceiling = fields.Float(string='Ceiling')
    ramp = fields.Float(string='Ramp')
    
    fffloor = fields.Float(string='Front First Floor')
    mumty = fields.Float(string='Mumty')
    squarter = fields.Float(string='Servant Quarter')
    wtank = fields.Float(string='Water Tank')
    
    lplot = fields.Boolean(string='Left Side')
    rplot = fields.Boolean(string='Right Side')
    fplot = fields.Boolean(string='Road')
    bplot = fields.Boolean(string='Back Side')
    
    notes = fields.Text(string='Notes', copy=False, default='Please mention Violations if any ...')
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
