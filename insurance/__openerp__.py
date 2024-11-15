# -*- coding: utf-8 -*-
{
    'name': "Insurance",

    'summary': """
        Create Insurance & Medical insurance over employee contract """,

    'description': """
    """,

    'author': "Dvit",
    'website': "http://www.Dvit.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'contract/insurance',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr','hr_contract','hr_payroll' ,'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
        'payroll_hr.xml',
    ],
    # only loaded in demonstration mode

}