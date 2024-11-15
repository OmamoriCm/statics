{
    'name': 'Multiple Payslip Confirm',
    'version': '1.0',
    'author': 'Khaled Hamed',
    'website': 'https://www.grandtk.com',
    'summary': 'Confirm Multiple Payslip at a same time.',
    'category': 'Human Resources',
    'license': 'AGPL-3',
    'depends': ['hr_payroll'],
    'data': [
        'views/pay_slip_view.xml',
        'wizard/pay_slip_wiz_view.xml',
    ],
    'description': """
        This Module is For verify & confirm Multiple Payslips at the same
        time...
    """,
    'images': ['static/img/main.png'],
    'auto_install': False,
    'installable': True,
}

