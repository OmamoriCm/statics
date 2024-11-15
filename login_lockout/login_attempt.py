# -*- encoding: utf-8 -*-
from openerp import SUPERUSER_ID
from openerp.osv import fields,osv
import datetime
from openerp.exceptions import Warning
from openerp import _

class login_attempt(osv.Model):
    _name = "login.attempt"
    _description = 'Login Attempts Counter'
    """
        # id - auto increment
        # address - IP address of client
        # datetime - datetime the user tried the login
    """
    _columns = {
        'remote_address': fields.char('Remote Address', readonly=True),
        'login_datetime': fields.datetime('Login Datetime', readonly=True),
        'failed_user_id': fields.char('Failed User', readonly=True),
    } 

    def create_login_line(self, cr, uid, remote_address, failed_user_id='', context=None):
        if remote_address:
            now = datetime.datetime.now()
            login_attempt_vals = {
                'login_datetime': now.strftime("%Y-%m-%d %H:%M:%S"),
                'remote_address': remote_address,
                'failed_user_id': failed_user_id,
            }
            new_created_attempt_id = self.create(cr, uid, login_attempt_vals, context=context)
            return new_created_attempt_id
        return False

    def check_login_attempts(self, cr, uid, remote_address, context=None):
        now = datetime.datetime.now()
        login_attempt_config_pool = self.pool.get('login.attempt.config')
        login_attempt_config_obj = login_attempt_config_pool.browse(cr, SUPERUSER_ID, uid, context=context)
        max_attempts_period = -(login_attempt_config_obj.max_attempts_period)
        max_attempts_num = login_attempt_config_obj.max_attempts_num
        now_minus_max_attempts_period = now + datetime.timedelta(minutes = max_attempts_period) #datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        search_clause =[('remote_address','=',remote_address),
                        ('login_datetime','<=', now.strftime("%Y-%m-%d %H:%M:%S")), #'01/18/2015 16:17:04'
                        ('login_datetime','>=', now_minus_max_attempts_period.strftime("%Y-%m-%d %H:%M:%S"))
                    ]
        login_attempt_ids = self.search(cr, SUPERUSER_ID, search_clause, order='id desc', limit=max_attempts_num) #, order='id desc', limit=5 , order='id asc', limit=5) #, order='id asc', limit=5
        if len(login_attempt_ids) < max_attempts_num:
            return False

        return True

login_attempt()