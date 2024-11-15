from openerp.osv import expression
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models, _

class courses(models.Model):

    _name = "courses"

    name = fields.Char(string="name" , required="True" ,translate="True")
    subjects = fields.Many2many('subjects', 'course_id','subject_id', 
        'course_subjects', string='subjects of course')


    @api.one
    def copy(self, default=None):
        default = dict(default or {})
        default.update(name=_("%s (copy)") % (self.name or ''))
        default.update(subjects=_("%s (copy)") % (self.subjects or ''))
        return super(courses, self).copy(default)


    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name of the course must be unique !'),
    ]