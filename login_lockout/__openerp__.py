# -*- coding: utf-8 -*-
##############################################################################
{
    'name': 'Login Lockout Mechanism',
    'version': '0.1',
    'category': 'Security',
    'author': 'Tamkeen Technologies',
    'website': 'http://tamkeentech.sa/',
    'description': """
Lockout Mechanism
########################################
    - Implements the lockout Mechanism.
    - The admin can configure the lockout mechanism, (e.g, 5 wrong attempts within 5 minutes).
    - The admin also can check/track/reenable the status of the inactive users who have been locked using the lockout mechanism.
""",
    'depends': ['base'],
    'data' : [
              'res_user_view.xml', 
              'login_attempt_config_view.xml',
              'login_attempt_view.xml',
              'module_menus.xml',
    ],
    'js': ['static/src/js/login_lockout.js'],
    'installable': True,
    'active': False,
}
