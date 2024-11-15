
from openerp.report import report_sxw
from openerp import models

class students_info_report2(report_sxw.rml_parse):
    

    def __init__(self, cr, uid, name, context):
        super(students_info_report2, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'line': self.set_context,
        })
        self.context = context
    

    def set_context(self, objects, data, ids, report_type=None):
        new_ids = ids

        if (data.get('wizard',False)):
            new_ids = data['form']['ids']
            objects = self.pool.get('students').browse(self.cr, self.uid, new_ids)
        
        return super(students_info_report2,self).set_context(objects,data,new_ids,report_type=report_type)

class schoolModul(models.AbstractModel):
    _name = 'report.student.students_info_report'
    _inherit = 'report.abstract_report'
    _template = 'schoolModul.students_info_report'
    _wrapped_report_class = students_info_report2

