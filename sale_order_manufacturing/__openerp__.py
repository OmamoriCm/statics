# -*- coding: utf-8 -*-
{
    'name': "Sales to Manufacturing Order",

    'summary': """
        Custom Sale Module that allows to create manufacturing orders directly from sales order""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Techspawn Solutions",
    'website': "https://techspawn.in",


    'category': 'Manufacturing',
    'version': '0.1',
    'application': True,
    "sequence": 1,
    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'sale', 'mrp'],

    'data': [
        'views/custom_sale_order_view.xml',
        'views/manufacturing_dropdown.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
}
