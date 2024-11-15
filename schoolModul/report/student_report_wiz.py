
from openerp.report import report_sxw
from openerp import report
from openerp import models

class students_info_report_wiz_cla(report_sxw.rml_parse):
    
    _name = 'student.wiz.report'

    def __init__(self, cr, uid, name, context):
        super(students_info_report_wiz_cla, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'line': self._get_students,
        })
        
        self.context = context

    def _get_students(self):

        #self.cr.execute("select v.name AS violation,p.name AS punishment,
        #m.penalty_amount AS penalty FROM hr_employee_violation AS m
        #left join hr_employee e on (m.employee_id=e.id)  
        #left join hr_punishment AS p on (m.punishment_id=p.id)
        #left join hr_violation AS v on (m.violation_id=v.id) where e.id=%s",(emp_id,)) 
        self.cr.execute("select * from students")
        res = self.cr.dictfetchall()
        return res
    
    '''
    def set_context(self, objects, data, ids, report_type=None):
        
        new_ids = ids

        if (data.get('wizard',False)):
            new_ids = data['form']['ids']
            objects = self.pool.get('students').browse(self.cr, self.uid, new_ids)

        return super(students_info_report_wiz_cla,self).set_context(objects,data,new_ids,report_type=report_type)
    '''

class school_stu_re_wiz(models.AbstractModel):
    _name = 'report.schoolModul.students_info_report_wiz'
    _inherit = 'report.abstract_report'
    _template = 'schoolModul.students_info_report_wiz'
    _wrapped_report_class = students_info_report_wiz_cla



