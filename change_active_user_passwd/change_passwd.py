# -*- coding: utf-8 -*-

from openerp.osv import fields, osv

class change_passwd(osv.osv):
    _name = 'aa.change_passwd'
    
    def _default_get_login(self):
        return self.env['res.users'].browse(self._uid).login
    
    _columns = {
    'login' : fields.char('Login', default=_default_get_login,readonly=True),
    'passwd' : fields.char('Password', required=True),
    }
    def change_passwd_button(self, cr, uid, ids, context=None):
        print('________change_passwd_button____')
#         self.ensure_one()
        data = self.read(cr, uid, ids, context=context)[0]
        encrypted = self.pool.get('res.users')._crypt_context(self, cr, uid, ids).encrypt(data['passwd'])
        cr.execute(
            "UPDATE res_users SET password='', password_crypt=%s WHERE id=%s",
            (encrypted, uid))
        cr.commit()
        return {
          'type': 'ir.actions.client',
          'tag': 'logout',
          }
