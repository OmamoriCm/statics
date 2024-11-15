# -*- encoding: utf-8 -*-
##############################################################################

from openerp.osv import fields,osv

class login_attempt_config_wizard(osv.osv_memory):
    _name = 'login.attempt.config.wizard'
    _inherit = 'res.config.settings'
    _columns = {
        'module_max_attempts_period': fields.integer('Max Attempts Period', help="The period that the system will allow for logging."),
        'module_max_unlock_period': fields.integer('Max Period To Unlock', help="The period that the system will unlock the user after it."),
        'module_max_attempts_num': fields.integer('Max Attempts Number', help="The maximum number of attempts the hacker can attempt in the given period."),
    }
    _defaults = {
        'module_max_attempts_period': lambda *a: 5, 
        'module_max_unlock_period': lambda *a: 5, 
        'module_max_attempts_num': lambda *a: 5, 
    }
    
    def default_get(self, cr, uid, fields, context=None):
        login_attempt_config_pool = self.pool.get('login.attempt.config')
        res = super(login_attempt_config_wizard, self).default_get(cr, uid, fields, context=context)
        login_attempt_config_ids = login_attempt_config_pool.search(cr, uid, [], context=context)
        if login_attempt_config_ids:
            login_attempt_config_obj = login_attempt_config_pool.browse(cr, uid, login_attempt_config_ids[0], context=context)
            vals = {
                    'module_max_attempts_period': login_attempt_config_obj.max_attempts_period,
                    'module_max_attempts_num': login_attempt_config_obj.max_attempts_num,
                    'module_max_unlock_period': login_attempt_config_obj.max_unlock_period,
            }
            res.update(vals)
        return res

    def save_record(self, cr, uid, ids, context=None):
        login_attempt_config_pool = self.pool.get('login.attempt.config')
        data = self.read(cr, uid, ids, context=context)[0]
        vals = {
                'max_attempts_period': data.get('module_max_attempts_period'),
                'max_unlock_period': data.get('module_max_unlock_period'),
                'max_attempts_num': data.get('module_max_attempts_num'),
        }
        login_attempt_config_ids = login_attempt_config_pool.search(cr, uid, [], context=context)
        if login_attempt_config_ids:
            login_attempt_config_pool.write(cr, uid, login_attempt_config_ids, vals, context=context)
        else:
            login_attempt_config_ids = login_attempt_config_pool.create(cr, uid, vals, context=context)
        return login_attempt_config_ids


class login_attempt_config(osv.Model):
    _name = "login.attempt.config"
    _description = 'Login Attempts Configuration'
    
    _columns = {
        'max_attempts_period': fields.integer('Max Attempts Period', help="The period that the system will allow for logging."),
        'max_unlock_period': fields.integer('Max Period To Unlock', help="The period that the system will unlock the user after it."),
        'max_attempts_num': fields.integer('Max Attempts Number', help="The maximum number of attempts the hacker can attempt in the given period."),
    } 

    _defaults = {
        'max_attempts_period': lambda *a: 5, 
        'max_unlock_period': lambda *a: 5, 
        'max_attempts_num': lambda *a: 5, 
    }


login_attempt_config_wizard()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
