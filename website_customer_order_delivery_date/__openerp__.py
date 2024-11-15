# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

{
    "name" : "Customer Order Delivery Date",
    "author" : "AppJetty",
    "version": "1.2",
    "category" : "Website",
    "website" : "https://goo.gl/2EJL4e",
    "description": "This module is used for add customer order delivery date section at payment page",
    "summary" : "Know when your customers want products delivered",
    "depends" : ['sale','website_sale'],
    "data":[
            'views/customer_order_delivery_config_view.xml',
            'views/sale_order_view.xml',
            'views/template.xml',
    ],
    'images': ['static/description/splash-screen.png'],
    # 'price': 10.00,
    # 'currency': 'EUR',
    'installable': True,
    'auto_install': False,   
    'support': 'support@appjetty.com',
}
