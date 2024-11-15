# -*- encoding: utf-8 -*-
import openerp
from openerp.osv import fields,osv
import datetime
from openerp.tools.translate import _

class track_export(osv.Model):
    _name = "track.export"
    _description = 'Track Data Export'

    _columns = {
        'user_name': fields.char('Responsible', readonly=True),
        'export_datetime': fields.datetime('Export Datetime', readonly=True),
        'exported_object': fields.char('Exported Object', readonly=True),
        'exported_fields': fields.text('Exported Object Fields', readonly=True),
        'exported_records_ids': fields.text('Exported Records IDs.', readonly=True, help="Empty value means that the user exported all the records."),
    } 

    def can_export(self, cr, uid, args, context=None):
        if self.pool.get('res.users').has_group(cr, uid, 'web_track_export.group_track_export'):
            return uid
        return 0

    def create_log_line(self, cr, uid, args, context=None):
        new_created_log_id = False
        if args:
            exported_object = args[0]
            exported_obj_fields = args[1]
            exported_records_ids = args[2] 
            now = datetime.datetime.now()
            user_obj = self.pool.get('res.users').browse(cr, uid, uid)
            user_name = user_obj.name
            
            export_log_vals = {
                'user_name': user_name,
                'export_datetime': now.strftime("%Y-%m-%d %H:%M:%S"),
                'exported_object': exported_object,
                'exported_fields': exported_obj_fields,
                'exported_records_ids': exported_records_ids,
            }
            new_created_log_id = self.create(cr, uid, export_log_vals, context=context)
        if new_created_log_id:
            self._notify_manager(cr, uid, new_created_log_id, context=context)
            return new_created_log_id
        return False

    def _notify_manager(self, cr, uid, ids, context=None):
        template_pool = self.pool.get('email.template')
        group_model_id = self.pool.get('ir.model').search(cr, uid, [('model', '=', 'track.export')])[0]
        body_html = '''<p>
Dear ${user.employee_ids[0].parent_id.name},
</p>
<p style="padding-left: 4em;">
<br>
As authorized by you earlier, ${user.name} has used the authorization and exported the following data from the system on ${object.export_datetime}:
<br>
<br>
Exported Fields:
<br>
${object.exported_fields}
<br>
Exported Records:
${object.exported_records_ids}
<br>
</p>
If you have concerns about this activity, please immediately <a href="mailto:erp@takamol.com.sa">Email Us</a>.
<br>
Thanks.
<br>
ERP System (Auto Generated Email)
'''
        template_data = {
            'model_id': group_model_id,
            'name': 'Data Exported',
            'subject' : 'Data Exported',
            # 'auto_delete': False,
            'body_html': body_html,
            'email_from' : '''${user.email}''', 
            'email_to' : '''${user.employee_ids[0].parent_id.work_email}''',
        }
        template_id = template_pool.search(cr, uid, [('model_id', '=', 'track.export'),('name','=','Data Exported')])
        if not template_id:
            template_id = template_pool.create(cr, uid, template_data, context=context)
        else:
            template_to_update = template_pool.write(cr, uid, template_id, template_data, context=context)
            template_id = template_id[0]
        template_pool.send_mail(cr, uid, template_id, ids, force_send=True, context=context)
        raise osv.except_osv(_('Success'), _('Data exported and your manager has been notified.'))
        return True