# -*- encoding: utf-8 -*-

# from functools import partial
# from lxml.builder import E
import openerp
from openerp import SUPERUSER_ID
from openerp import pooler #, tools
from openerp.osv import fields,osv
import logging

_logger = logging.getLogger(__name__)
import datetime

class res_users(osv.Model):
    _inherit = 'res.users'

    _columns = { 
            # 'session_id' : fields.char('Session Id', size=100), 
            # 'expiration_date' : fields.datetime('Expiration Date'), 
            'deactivate_reason': fields.selection([('hacked','Hacked'),('locked','Locked')],'Last Deactivation Reason'),
            'deactivate_time': fields.datetime('Last Deactivation Time', readonly=True),  
            'activate_time': fields.datetime('Last Activation Time', readonly=True),  
    } 

    #     return user_id
    def authenticate(self, db, login, password, user_agent_env):
        """Verifies and returns the user ID corresponding to the given
          ``login`` and ``password`` combination, or False if there was
          no matching user.

           :param str db: the database on which user is trying to authenticate
           :param str login: username
           :param str password: user password
           :param dict user_agent_env: environment dictionary describing any
               relevant environment attributes
        """
        uid = self._login(db, login, password)
        if uid == openerp.SUPERUSER_ID:
            # Successfully logged in as admin!
            # Attempt to guess the web base url...
            if user_agent_env and user_agent_env.get('base_location'):
                cr = pooler.get_db(db).cursor()
                try:
                    base = user_agent_env['base_location']
                    ICP = self.pool.get('ir.config_parameter')
                    if not ICP.get_param(cr, uid, 'web.base.url.freeze'):
                        ICP.set_param(cr, uid, 'web.base.url', base)
                    cr.commit()
                except Exception:
                    _logger.exception("Failed to update web.base.url configuration parameter")
                finally:
                    cr.close()

        if not uid:
            if user_agent_env and user_agent_env.get('base_location'):
                cr = pooler.get_db(db).cursor()
                try:
                    remote_address = user_agent_env['REMOTE_ADDR']
                    login_attempt_pool = self.pool.get('login.attempt')
                    failed_user_id = self.search(cr, SUPERUSER_ID, [('login','=',login)])
                    if failed_user_id:
                        user_info = str(login) +' with ID: '+ str(failed_user_id[0])
                    else:
                        user_info = str(login)
                    login_attempt_pool.create_login_line(cr, SUPERUSER_ID, remote_address, user_info)
                    cr.commit()
                    ### for counting the number of failed attempts
                    exceeded_limit = login_attempt_pool.check_login_attempts(cr, SUPERUSER_ID, remote_address)
                    if exceeded_limit:
                        if failed_user_id:
                            self.lock_user(cr, SUPERUSER_ID, failed_user_id)
                except Exception:
                    _logger.exception("Failed to create a new failed login attempt.")
                finally:
                    cr.close()

        return uid

    def lock_user(self, cr, uid, failed_user_id):
        try:
            # cr.autocommit(True)
            cr.execute("UPDATE res_users SET active=False, deactivate_time=now() AT TIME ZONE 'UTC', deactivate_reason='hacked' WHERE id=%s", (failed_user_id[0],)) #id=%s RETURNING id", (failed_user_id[0],))
            # , deactivate_time=now() AT TIME ZONE 'UTC'
            cr.commit()
        except Exception:
            _logger.debug("Failed to deactivate the user with login:%s", login, exc_info=True)
        # finally:
        #     cr.commit()
        #     #cr.close() 
        return True

    def cron_unlock_users(self, cr, uid, context=None):
        if context is None:
            context = {}

        login_attempt_config_pool = self.pool.get('login.attempt.config')
        login_attempt_config_obj = login_attempt_config_pool.browse(cr, uid, uid, context=context)
        max_attempts_period = -(int(login_attempt_config_obj.max_attempts_period))
        
        now = datetime.datetime.now()
        now_minus_max_attempts_period = now + datetime.timedelta(minutes = max_attempts_period) #datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        search_clause =[('deactivate_reason','=','hacked'),
                        ('active','=',False),
                        # ('deactivate_time','<=', now.strftime("%Y-%m-%d %H:%M:%S")), #'01/18/2015 16:17:04'
                        ('deactivate_time','<=', now_minus_max_attempts_period.strftime("%Y-%m-%d %H:%M:%S")),
                    ]
        # locked_users_ids = self.search(cr, SUPERUSER_ID, search_clause) #, order='id desc', limit=5 , order='id asc', limit=5) #, order='id asc', limit=5
        locked_users_ids = self.search(cr, uid, search_clause)
        for user_id in self.browse(cr, uid, locked_users_ids, context):
            try:
                # cr.autocommit(True)
                cr.execute("UPDATE res_users SET active=True, activate_time=now() AT TIME ZONE 'UTC' WHERE id=%s", (user_id.id,)) #id=%s RETURNING id", (failed_user_id[0],))
                # , deactivate_time=now() AT TIME ZONE 'UTC'
                cr.commit()
            except Exception:
                _logger.debug("Failed to deactivate the user with login:%s", login, exc_info=True)
        return True

res_users()
