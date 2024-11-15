from openerp import api, fields, models, _
from openerp.exceptions import Warning

class hr_employee(models.Model):
	_inherit = 'hr.employee'

	otherid = fields.Integer('Biometric Login ID')

	@api.multi
	@api.constrains('work_email')
	def _check_work_email(self):
		for employee in self:
			if employee.work_email and len(employee.search([('work_email','=',employee.work_email)])) > 1:
				raise ValueError(_('This email is already registered'))