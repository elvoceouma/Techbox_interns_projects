# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Rental',
    'version': '1.0',
    'category': 'Productivity',
    'summary': 'Rental management module for Odoo',
    'website': 'https://techbox.ke',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/rental_core_views.xml',
        'views/menu_action_views.xml',
        'views/rental_views.xml',
        
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
