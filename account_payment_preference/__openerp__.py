# -*- coding: utf-8 -*-

######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

{
    "name" : "Account Payment Preference",
    "version" : "1.8",
    "author" : "Ursa Information Systems",
    "category" : "Accounting & Finance",
    "summary": "Payment Preference on Partners, Invoices and Payments (Ursa)",
    'description':
        """ 
Overview 
-------- 
For version 8.0, this module adds a new attribute to the Partner form view called 'Payment Preference' which records the 
preferred method used by this partner to make or receive payments. This is carried over to Invoices and Payments (where it can be changed). 

Developer Notes 
--------------- 
* OpenERP Version: 8.0 
* Ursa Dev Team: RC 

Contact 
------- 
* contact@ursainfosystems.com
        """,
    "maintainer": 'Ursa Information Systems',
    "website": 'http://www.ursainfosystems.com',
    'images': ['static/description/partner_payment_pref.png','static/description/invoice_payment_pref.png','static/description/payment_payment_pref.png'],
    "depends" : ["base", "account_accountant","account_voucher"],
    "init_xml" : [],
    "demo_xml" : [],
    "data" : [
        'views/account_invoice.xml',
        'views/account_voucher.xml',
        'views/res_partner.xml',
        'views/ir_ui.xml',
        'security/ir.model.access.csv',
    ],
    "test" : [
    ],
    "auto_install": False,
    "application": False,
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
