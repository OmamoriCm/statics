# -*- coding: utf-8 -*-
{
    'name': "Product Export Id Generator",

    'summary': """
        Creates Product Export ID while creating a Product, which will be used while importing product related data.""",

    'description': """
        Creates Product Export ID while creating a Product, which will be used while importing product related data.
    """,

    'author': "TechsSpawn Solutions",
    'website': "www.techspawn.com",

    'category': 'Product',
    'version': '0.1',
    'images': ['static/description/main.png'],

    # any module necessary for this one to work correctly
    'depends': ['base', 'product'],

    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
}