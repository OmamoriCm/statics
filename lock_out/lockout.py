from openerp.osv import osv, fields
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import logging
from openerp.tools.translate import _
from openerp import api, tools
from dateutil.relativedelta import *
from openerp import SUPERUSER_ID
#from openerp.tools import html2plaintext
#import math
#import re

_logger = logging.getLogger(__name__)

class res_company(osv.osv):    
    _inherit = "res.company"
    _columns={
                'lockouttime_id': fields.many2one('lockout.time', 'Un-lock After'),
                'attempt_cnt':fields.selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10')],'No. of Attempts'),
              }
    _defaults={
               'attempt_cnt':lambda obj, cr, uid, context:'3',
               }
               
    # Scheduler
    
    def run_scheduler_lockout(self, cr, uid, context=None):
        '''
        Call the scheduler to Un-lock the Users.
        '''
        if context is None:
            context = {}
        current = datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        lockids  = self.pool.get('res.users').search(cr, uid, [('flg_userlocked','=',True)])
        company_ids = self.pool.get('res.company').search(cr, uid, [])
        company = self.pool.get('res.company').browse(cr, uid, company_ids[0])
        attempt_cnt = company.attempt_cnt
        unlock_after = company.lockouttime_id.value
        for lock in self.pool.get('res.users').browse(cr, uid, lockids, context=context):
            if int(unlock_after)!=0:
                diff=(current-(datetime.strptime(lock.userlocked_datetime, '%Y-%m-%d %H:%M:%S')+timedelta(minutes=int(unlock_after))))
                if diff.days>=0 and diff.seconds>0:
                    lock.userlocked_datetime = False
                    lock.flg_userlocked = False
                    lock.wronglogin_cnt = 0
        return {}

class lockout_time(osv.osv):    
    _name = "lockout.time"
    _order = "sequence"
    _columns={
                'name': fields.char('Name',required=True),
                'value':fields.integer('Time in Minutes',help='Give 0 for not to Un-lock Automatically',required=True),
                'sequence':fields.integer('Sequence',required=True),
              }
              
lockout_time()

class res_users(osv.osv):    
    _inherit = "res.users"
    _columns={
                'flg_userlocked': fields.boolean('User Locked?'),
                'userlocked_datetime': fields.datetime('User locked Date Time'),
                'wronglogin_cnt':fields.integer('Wrong Login Count'),
              }
    _defaults={
               'flg_userlocked':lambda obj, cr, uid, context:False,
               'wronglogin_cnt':0,
               }
    def onchange_flg_userlocked(self, cr, uid, ids, flg, context=None):
        ret ={}
        for user in self.browse(cr, uid, ids, context=context):
            if flg:
                ret['flg_userlocked']= True
                ret['userlocked_datetime'] = time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                ret['flg_userlocked'] = False
                ret['userlocked_datetime'] = False
                ret['user.wronglogin_cnt'] = 0
        return {'value':ret}

        
