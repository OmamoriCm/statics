from openerp.osv import expression
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models, _
from datetime import date,datetime


class students(models.Model):
	
	_name = "students"

	code = fields.Char(required=True, size=8)
	user_id = fields.Many2one('res.users', string='User ID',ondelete="cascade",
							 select=True, required=True)

	name = fields.Char(related='user_id.name', string="student name" ,
							store=True, readonly=True, translate="True")

	email = fields.Char(related='user_id.login' ,string="Email" , translate="True")
	date_of_birth = fields.Date(string="student birth date", required="True")
	mobile = fields.Char(string="student mobile")
	parent_ids = fields.Many2one('parents',string="parent_id")
	last_login_date = fields.Date(string="last_login_date",readonly=True)
	course_id = fields.Many2one('courses',string="course")
	last_login_ip = fields.Char(string="last_login_ip",readonly=True)
	date_of_joint = fields.Date(string="date of joint")
	status = fields.Selection([
                     ('draft', 'Draft'),
                     ('experiment', 'In Experiment'),
                     ('approved', 'In Service'),
                     ('refuse', 'Out of Service')], default='draft')
	patch = fields.Char(string="Patch" , required = True)
	
	stop_date = fields.Date(string="student ending date", required="True")	



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

 	@api.one
	def copy(self, default=None):
		default = dict(default or {})
		default.update(name=_("%s (copy)") % (self.name or ''))
		default.update(email=_("%s (copy)") % (self.email or ''))
		return super(students, self).copy(default)


	_sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name of the student must be unique !'),
	]
