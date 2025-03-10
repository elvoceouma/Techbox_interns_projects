# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Apprentice',
    'version': '1.0',
    'category': 'Productivity',
    'summary': 'Apprenticeship module for Odoo',
    'website': 'https://techbox.ke',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu_action_views.xml',
        'views/apprentice_core_views.xml',
        
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
