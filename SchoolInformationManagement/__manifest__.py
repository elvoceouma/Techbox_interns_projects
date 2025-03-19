# Manifest data => Apps metadata 

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'School Managements',
    'version': '1.0',
    'category': 'Productivity',
    'summary': 'A   digital school management system platform for unified school records and data consolidation ',
    'author': "Maria Goretti",
    'website': 'https://techbox.ke',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
       'security/ir.model.access.csv',
        'views/learner_core_views.xml',  
        'views/teachers_core_views.xml', 
        'views/subjects_core_views.xml',
        'views/parents_core_views.xml',
        'views/menu_action_views.xml',
         
   
        
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
