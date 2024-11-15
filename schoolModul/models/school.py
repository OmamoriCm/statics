
#import time
#import math
#from openerp.tools.float_utils import float_round as round
#from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

from openerp.osv import expression
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models, _
from datetime import date,datetime

class teachers(models.Model) :

	_name = "teachers"

	code = fields.Char(required=True)
	name = fields.Char(string="teacher name" , required="True" , translate="True")
	email = fields.Char(string="Email" , translate="True")
	date_of_birth = fields.Date(string="teacher birth date")
	mobile = fields.Char(string="teacher mobile")
	last_login_date = fields.Date()
	last_login_ip = fields.Char()
	date_of_joint = fields.Date(string="date of joint")
	status = fields.Selection([
                     ('draft', 'Draft'),
                     ('experiment', 'In Experiment'),
                     ('approved', 'In Service'),
                     ('refuse', 'Out of Service')], default='draft')
	classroom_id  = fields.Many2one('classroom',string="classroom")

	teacher_salary = fields.Float(string='the Amount',compute='_compute_teach_salary',
		store=True)



	@api.one
	@api.depends('status')
	def _compute_teach_salary(self):

		if self.status == 'approved' :
			self.teacher_salary = 4000;
		elif self.status == 'experiment' :
			self.teacher_salary = 2000;
		else :
			self.teacher_salary = 0;



	@api.multi
	@api.constrains('email')
	def _check_email(self):
		if self.email :
			if any((c in "@" )for c in self.email):
				return True
			else :
				raise ValidationError(_('invaild email'))
		
			

	
	@api.onchange('date_of_birth')
	def onchange_birth_birth_date(self):

		fmt = '%Y-%m-%d'
		if not self.date_of_birth :
			self.date_of_birth = date.today()

		bir_da = datetime.strptime(str(self.date_of_birth),fmt)
		to_day = datetime.strptime(str(date.today()),fmt)

		if bir_da > to_day :
			raise ValidationError(_('date of birth is in the future  !!'))
	
	

	@api.onchange('date_of_joint')
	def onchange_birth_joint_date(self):
		""" this function is checking date of joint if in the 
		future raise message """

		fmt = '%Y-%m-%d'
		if not self.date_of_joint :
			self.date_of_joint = date.today()

		d_of_jo = datetime.strptime(str(self.date_of_joint),fmt)
		to_day = datetime.strptime(str(date.today()),fmt)

		if d_of_jo > to_day :
			raise ValidationError(_('the date of join is in the future !!'))
        
	
	
	_sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name of the student must be unique !'),
	]

	@api.multi
	def refuse(self):

		self.write({'status': 'refuse'})
		return True

	@api.multi	
	def experiment(self):

		self.write({'status': 'experiment'})
		return True

	@api.multi	
	def approved(self):

		self.write({'status': 'approved'})
		return True

	@api.multi	
	def set_to_draft(self):

		self.write({'status': 'draft'})
		return True



class classroom(models.Model) :

	_name = "classroom"

	sequence = fields.Char(readonly=True, default='/')
	name = fields.Char(string="classroom name" , required="True" , translate="True")
	student_class_room = fields.Many2many('students', 'student_class_room','student_id', 
		'classroom_id', string='sudents class room')
	grade_id = fields.Many2one('grades',string="grade")
	section = fields.Char(string="section")
	status = fields.Boolean(string="classroom status" , default="false")
	remarks = fields.Char(string="remark",required="True")
	teacher_id = fields.Many2one('teachers',string="teacher")


_sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name of the student must be unique !'),
   ]


class parents(models.Model) :

	_name = "parents"


	code = fields.Char(string="Code",required=True)
	name = fields.Char(string="parent name" , required="True" , translate="True")
	student_id = fields.Many2one('students',string="student id")
	email = fields.Char(string="Email" , translate="True")
	date_of_birth = fields.Date(string="parent birth date")
	mobile = fields.Char(string="parent mobile")
	date_of_joint = fields.Char(string="date of joint")
	status = fields.Boolean(string="parent status" , default="false")


	_sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name of the student must be unique !'),
    ]
	@api.multi
	def refuse(self):

		self.write({'status': 'refuse'})
		return True

	@api.multi	
	def experiment(self):

		self.write({'status': 'experiment'})
		return True

	@api.multi	
	def approved(self):

		self.write({'status': 'approved'})
		return True

	@api.multi	
	def set_to_draft(self):

		self.write({'status': 'draft'})
		return True




class exams(models.Model) :

	_name = "exams"

	code = fields.Char(string="code" ,required=True) 
	name = fields.Char(string="name" , required="True")
	exam_type = fields.Many2one('exam_type', string="exam type")
	start_date = fields.Date(string="start_date")
	students_ = fields.Many2many('students','student_exams','exam_c','stu_c',string ="students_exam")


	@api.model
	def name_search(self, name, args=None, operator='ilike', limit=100):
		""" this function didn't work the target from function 
		to show only the exam that was not selected for the active student 
		by other words i wnat to ensure that the student has just one selected exam
		at the time  """
		
		args = args or []
		recs = self.browse()
		exam_resu = self.env['exam_results'].search([],limit=4)

		print "@@@@@ exam_resu", exam_resu.student_id
		print "@@@@@ rec before",recs

		if name:
			for line in self :
				recs = self.search([(line.exam_resu.student_id, '=',line.students_.id)] + args, limit=limit)
				rec = []
				break
		if not recs:
			recs = self.search([('name', operator, name)] + args, limit=limit)

		print "@@@@@@@@@ rec after"
		return recs.name_get()
	
	_sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name of the student must be unique !'),
    ]
class exam_results(models.Model) :

	_name = "exam_results"

	student_id = fields.Many2one('students',string="student", required="True")
	exam = fields.Many2one('exams',string="Exam", required="True")
	subject = fields.Many2one('subjects',string="subject", required="True")
	marks = fields.Float(string="marks",required="True")

	



class attendance(models.Model) :

	_name = "attendance"

	#student_id = fields.Many2one('students',string="student", required="True")
	date = fields.Date(string="date")
	remarks = fields.Char(string="remark",required="True")
	#Batch
	#course


	############# these features did not apply in the system ###############################
	# this main attendance Registers , i must add another model to  (attendance sheet )
	# that shows Register which configuar in above model and the code of register and its name 
    # and the date and will be in (attendance sheet ) tab of ( students) which contains student
    # and is it persent ? (state boolean) and remark if found .
    # the total of Persent and total of absent .






class grades(models.Model) :

	_name = "grades"

	code = fields.Char(required=True) 
	name = fields.Char(string="grades name" , required="True" , translate="True")
	desc = fields.Char(string="description")





class subjects(models.Model) :

	_name = "subjects"

	code = fields.Char(required=True) 
	name = fields.Char(string="name",required=True)
	maximum_marks = fields.Integer("Maximum marks")
	minimum_marks = fields.Integer("Minimum marks")
	#teacher_ids = fields.Many2many('hr.employee', 'subject_teacher_rel', 'subject_id', 'teacher_id', 'Teachers')
	description = fields.Text(string="description")
	student_ids = fields.Many2many('students','elective_subject_student_rel', 'subject_id', 'student_id', 'Students')
	grade_id = fields.Many2one('grades',string="grade")



	_sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name of the subject must be unique !'),
	]


class exam_type(models.Model) :

	_name = "exam_type"

	name = fields.Char(string="name" , required="True")
	description = fields.Char(string="description")






# these features didnot applied yet .
# need analysis 

'''

class StudentPreviousSchool(models.Model):
    
    _name = "student.previous.school"
    _description = "Student Previous School"

    previous_school_id = fields.Many2one('student.student', 'Student')
    name = fields.Char('Name', required=True)
    registration_no = fields.Char('Registration No.', required=True)
    admission_date = fields.Date('Admission Date')
    exit_date = fields.Date('Exit Date')
    course_id = fields.Many2one('standard.standard', 'Course', required=True)
    add_sub = fields.One2many('academic.subject', 'add_sub_id',
                              string='Add Subjects')


class StudentHistory(models.Model):
    _name = "student.history"

    student_id = fields.Many2one('students', 'Student')
    academice_year_id = fields.Many2one('academic.year', 'Academic Year',
                                        required=True)
    standard_id = fields.Many2one('school.standard', 'Standard',
                                  required=True)
    percentage = fields.Float("Percentage", readonly=True)
    result = fields.Char(string='Result', readonly=True, store=True)


class StudentCertificate(models.Model):
    _name = "student.certificate"

    student_id = fields.Many2one('student.student', 'Student')
    description = fields.Char('Description')
    certi = fields.Binary('Certificate', required=True)


class HrEmployee(models.Model):

    _name = 'hr.employee'
    _inherit = 'hr.employee'
    _description = 'Teacher Information'

    @api.one
    def _compute_subject(self):
        This function will automatically computes the subjects related \
                                                   to particular teacher
        subject_obj = self.env['subject.subject']
        subject_ids = subject_obj.search([('teacher_ids', '=', self.id)])
        sub_list = []
        for sub_rec in subject_ids:
            sub_list.append(sub_rec.id)
        self.subject_ids = sub_list

    subject_ids = fields.Many2many('subject.subject', 'hr_employee_rel',
                                   compute='_compute_subject',
                                   string='Subjects')
'''