# -*- coding: utf-8 -*-
################################################################################
#                                                                              
#                        Module [Devis_en_lettres]                         
#                    ----------------------------------                        
#                      permet d'ajouter une convertion                         
#                        du total en lettres (Devis)                           
#                    ----------------------------------                        
#                                                                              
#                       langage : Python 2.7                                   
#                       date creation : 20/08/2015                             
#                       date modification : 25/08/2015                         
#                       version : 0.1                                          
#                       auteur  : MLMConseil                              
#                                                                              
################################################################################
{
    'name': "Devis_en_lettres",

    'summary': """
        Conversion du Total d'un devis en lettres (Dinar Algérien)""",

    'description': """
        Conversion du Total d'un devis en lettres (Dinar Algérien)...
    """,

    'author': "MLMConseil",
    'website': "http://www.mlmconseil.dz",
    #'sequence': 3,

    'category': 'Sale',
    'version': '0.1',

    'depends': ['base','sale'],

    
    'data': [
        # 'security/ir.model.access.csv',
        'Devis_en_lettres.xml',
        'views/report_saleorder.xml'
		
    ],
    
    # 'demo': [
    #     'demo.xml',
    #],
    'installable': True,
    #'application': False,
    'auto_install': False,
}