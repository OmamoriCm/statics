# -*- coding: utf-8 -*-

{
    'name': 'Email Marketing Bounce',
    'version': '1.0',
    'category': 'Tools',
    'sequence': 1,
    'summary': 'Opt out Bounced customers from mailing campaigns.',
    'description': """
Opt out Bounced customers from mailing campaigns to avoid unnecessary load while performing Email Campaigns.
------------------------------------------------------------------------------------------------------------

    """,
    'author': 'MSP1 Managed IT Services Pvt Ltd.',
	'website': 'http://www.msp1services.com',
    'depends': ['mass_mailing'],
    'data': [
        'bounce_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
