# -*- coding: utf-8 -*-

{
    'name': 'Rahisi',
    'version': '1.0',
    'category': 'Services',
    'summary': 'Apprenticeship module for Odoo',
    'author' : 'Hafsah Siti',
    'website': 'https://techbox.ke',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/rahisi_security.xml',
        'security/ir.model.access.csv',
        'views/rahisi_core_views.xml',
        'views/rahisi_service_provider_views.xml',
        'views/rahisi_service_views.xml',
        'views/rahisi_service_category_views.xml',
        'views/rahisi_job_views.xml',
        'views/rahisi_review_views.xml',
        'views/rahisi_customer_views.xml',
        'views/menus.xml',
        
     
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
