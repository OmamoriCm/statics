# -*- encoding: utf-8 -*-

##############################################################################
#
#    Samples module for Odoo 8
#    Copyright (c) 2018 Copyright (c) 2018 aek
#      Anicet Eric Kouame <anicetkeric@gmail.com>
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
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from datetime import date

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import netsvc



class hr_employee_degree(osv.osv):
    _name = "hr.employee.degree"
    _description = "Degree of employee"
    _columns = {
        'name': fields.char('Name', required=True, translate=True),
        'sequence': fields.integer('Sequence', help="Gives the sequence order when displaying a list of degrees."),
    }
    _defaults = {
        'sequence': 1,
    }
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name of the Degree of employee must be unique!')
    ]
hr_employee_degree()


class licence(osv.osv):
    _name = "hr.licence"
    _description = "Licence of employee"
    
    _columns={
              'name':fields.char('Name', size=64, required=True, readonly=False),
              'reference':fields.char('Reference', size=64, required=False, readonly=False),
              'start_date':fields.date('Start Date'),
              'end_date':fields.date('End Date'),
              'employee_id':fields.many2one('hr.employee', 'Employee', required=False),
              }
licence()


class graduate_domain(osv.osv):
    _name = "hr.graduate.domain"
    _description = "graduate domain"
    _columns={
              'libelle':fields.char('Name', size=64, required=True, readonly=False),
              }
graduate_domain()

class hr_employee_graduate(osv.osv):
    _name = "hr.employee.graduate"
    _description = "graduate of the employee"

    _columns={
              'name':fields.char('Name', size=64, required=False, readonly=False,translate=True),
              'grade_id':fields.many2one('hr.employee.degree', 'Level', required=True),
              'domain_id':fields.many2one('hr.graduate.domain', 'Domain',required=False, readonly=False),
              'reference':fields.char('Reference', size=64, required=False, readonly=False),
              'date_obtention':fields.date("Date of obtaining"),
              'start_date':fields.date("Start Date"),
              'end_date':fields.date("End Date"),
              'type':fields.selection([('graduates','graduates'),('certif','Certification')],"Type",select=True),
              'image':fields.binary('Image'),
              'employee_id':fields.many2one('hr.employee', 'Employee', required=False)
              }
hr_employee_graduate()


class visa(osv.osv):
    _name = "hr.visa"
    _description = "employee visa"

    _columns={
              'name':fields.char('visa title', size=64, required=True, readonly=False),
              'reference':fields.char('N° Visa', size=64, required=True, readonly=False),
              'pays_id': fields.many2one('res.country', 'Pays', required=True),
              'start_date':fields.datetime('Start Date'),
              'end_date':fields.datetime('End Date'),
              'employee_id':fields.many2one('hr.employee', 'Employee', required=False)
              }
visa()

class residence_permit(osv.osv):
    _name = "hr.residence.permit"
    _description = "residence permit of the employee"

    _columns={
              'name':fields.char('Permit title', size=64, required=False, readonly=False),
              'reference':fields.char('N° permit', size=64, required=False, readonly=False),
              'pays_id': fields.many2one('res.country', 'Pays', required=False),
              'start_date': fields.datetime('Start Date'),
              'end_date': fields.datetime('End Date'),
              'employee_id':fields.many2one('hr.employee', 'Employee', required=False)
              }
residence_permit()


class hr_employee_children(osv.osv):
    _name = "hr.employee.children"
    _description = "employee's children"
    
    _columns={
              'name': fields.char('Nom', size=128, required=True, readonly=False),
              'birthday': fields.date("Date of Birth"),
              'birth_place': fields.char("place of birth"),
              'mobile': fields.char('Mobile', size=128, required=False, readonly=False),
              'gender': fields.selection([('male', 'Male'), ('female', 'Female')], 'Gender'),
              'employee_id': fields.many2one('hr.employee', 'Employee', required=False),
              }    
hr_employee_children()


class hr_employee_parents(osv.osv):
    _name="hr.employee.parents"
    _description = "the parents of the employee"
    _columns = {
            
              'name':fields.char('Nom', size=128, required=True, readonly=False),
              'birthday': fields.date("Date of Birth"),
              'birth_place': fields.char("place of birth"),
              'mobile': fields.char('Mobile', size=128, required=False, readonly=False),
              'gender': fields.selection([('male', 'Male'), ('female', 'Female')], 'Gender'),
              'email': fields.char('email', size=128, required=False, readonly=False),
              'employee_id': fields.many2one('hr.employee', 'Employee', required=False),
        } 

hr_employee_parents()


class hr_employee_emergency(osv.osv):
    _name = 'hr.employee.emergency'
    _description = 'Emergency Contact'
    _columns = {
        'name':fields.char("Name",size=128,required=True),
        'email':fields.char("Email",size=128),
        'mobile': fields.char('Mobile',size=128, required=True),
        'relation': fields.selection([('father', 'Father'), ('mother', 'Mother'), ('daughter', 'Daughter'), ('son', 'Son'),('wife', 'Wife')], string='Relationship', help='Relation with employee', select=True, readonly=True),
        'employee_id': fields.many2one("hr.employee", 'Employee'),
        }  
hr_employee_emergency()

class hr_type_piece(osv.osv):
    _name="hr.type.piece"
    _description="Type of identity document"
    _columns={
              'name':fields.char("Title",size=128,required=True),
              "description":fields.text("Description"),
              }
hr_type_piece()


class hr_piece_identite(osv.osv):
    _name="hr.piece.identite"
    _rec_name="numero_piece"
    _decription="Id Card"
    _columns={
              'numero_piece':fields.char("Id",size=128,required=True),
              'nature_piece':fields.selection([('attestion',"Certificate of identity"),("working_license","working license"),
                                               ("cni","CNI"),("passport","Passport")],string="Nature",required=True),
              'established_date':fields.date("Established Date",required=True),
              'image': fields.binary('Image'),
              'authority':fields.char("Authority",size=128),
              }
hr_piece_identite()


class hr_employee(osv.osv):
    _inherit="hr.employee"
    _columns={
              'father':fields.char('Father name', size=128, required=False, readonly=False),
              'mother':fields.char('mother Name', size=128, required=False, readonly=False),
              'grade':fields.char('Grade', size=64, required=False, readonly=False),
              'childrens_ids':fields.one2many('hr.employee.children', 'employee_id', 'Childrens', required=False),
              'licence_ids': fields.one2many('hr.licence', 'employee_id', 'Licence of employee'),
              'graduate_ids': fields.one2many('hr.employee.graduate', 'employee_id', 'Graduate of the employee'),
              'visa_ids': fields.one2many('hr.visa', 'employee_id', 'employee visa'),
              'residence_permit_ids': fields.one2many('hr.residence.permit', 'employee_id', 'Residence permit'),
              'payment_method':fields.selection([('cash','Cash'),('transfer','Bank transfert'),('check','Checks')],
                                                string='Payment Method',required=True),
              'date_entry':fields.date("Date entry"),
              'blood_type': fields.selection([('o', 'O'), ('a', 'A'), ('b', 'B'), ('ab', 'AB')],
                                           string='Blood Type', required=False),
              'piece_identite_id':fields.many2one("hr.piece.identite","Id Card"),
              'emergency_contact_ids': fields.one2many('hr.employee.emergency','employee_id','Emergency Contact'),
              'parent_employee_ids':fields.one2many("hr.employee.parents",'employee_id','parents of the employee'),
              'recruitment_degree_id':fields.many2one('hr.employee.degree',"Degree of employee"),
              }
    _defaults={
               'marital':'single',
               'payment_method':'transfer',
               }
hr_employee()