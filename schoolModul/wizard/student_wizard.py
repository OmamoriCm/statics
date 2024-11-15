from openerp.osv import fields, osv
from openerp.exceptions import UserError, ValidationError

class student_wizard(osv.osv_memory):

    _name = 'student.wizard'
    
    _description = 'Wizard to print student report'

    _columns = {
        'student_ids': fields.many2many('students', 
                                        'stud_stud_wizard_rel', 
                                        'wizard_id', 'id', 
                                        'student', required=True),
    }

    def print_report(self, cr, uid, ids, context=None):
               
        if context is None:
            context = {}
        data = self.read(cr, uid, ids,context=context)[0]
        datas = {
             'ids': context.get('active_ids', []),
             'model': 'students',
             'form': data
                }
        datas['form']['ids']=datas['ids']

        return self.pool['report'].get_action(cr, uid, [], 'schoolModul.students_info_report_wiz', data=datas, context=context)