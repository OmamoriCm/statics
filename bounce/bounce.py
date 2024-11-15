# -*- coding: utf-8 -*-

from openerp import fields, models

class MassMailingContact(models.Model):
	_inherit = 'mail.mass_mailing.contact'
	
	is_bounced = fields.Boolean(string='Bounced', help='The contact has bounced and should not receive mails anymore')

class MailMailStats(models.Model):
	_inherit = 'mail.mail.statistics'
	
	def _process_bounced_mails(self, cr, uid, context=None):
		contact_ids = []
		bounced_ids = self.search(cr, uid, [('bounced', '!=', False)], context=context)
		for contact_id in self.read(cr, uid, bounced_ids, ['res_id'], context=context):
			contact_ids.append(contact_id['res_id'])
		contact_obj = self.pool.get('mail.mass_mailing.contact')
		bounced_emails = contact_obj.search(cr, uid, [('id','in',contact_ids),('is_bounced','=',False)])
		contact_obj.write(cr, uid, bounced_emails, {'opt_out': True, 'is_bounced': True})