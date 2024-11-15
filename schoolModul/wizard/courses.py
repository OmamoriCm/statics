from openerp.osv import fields, osv
from openerp.exceptions import UserError, ValidationError
from openerp import api, fields, models

class course_wizard(models.Model):

    _name = 'course.wizard'
    
    start_date = fields.Date("Start Date", required= True)
    end_date = fields.Date("End Date" ,required= True)

    _description = 'Wizard to print courses report'


    def check_report(self, cr, uid, ids, context=None):
               
        if context is None:
            context = {}
        data = self.read(cr, uid, ids,context=context)[0]
        datas = {
             'ids': context.get('active_ids', []),
             'model': 'courses',
             'form': data
                }
        datas['form']['ids']=datas['ids']
        return self.pool['report'].get_action(cr, uid, [], 'schoolModul.courses_info_wiz', data=datas, context=context)