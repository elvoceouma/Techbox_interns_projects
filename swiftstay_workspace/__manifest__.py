

{
    'name': 'SwiftStay',
    'version': '1.0',
    'category': 'Services',
    'summary': 'Hotel check-in module for Odoo',
    'website': 'https://techbox.ke',
    'author': 'Zahabiya Shamoon',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/swiftstay_core_views.xml',
        'views/swiftstay_amenities_views.xml',
        'views/swiftstay_room_types_views.xml',
        'views/swiftstay_rooms_views.xml',
        'views/swiftstay_booking_views.xml',
        'views/swiftstay_invoice_views.xml',
        'views/menu.xml',
        
        
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}