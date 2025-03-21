

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
        'account',
        'website',
        
        
    ],
    'data': [
        'security/swiftstay_security.xml',
        'security/ir.model.access.csv',
        'views/swiftstay_core_views.xml',
        'views/swiftstay_rooms_views.xml',
        'views/swiftstay_amenities_views.xml',
        'views/swiftstay_room_types_views.xml',
        'views/swiftstay_booking_views.xml',
        'views/swiftstay_room_details_template.xml',
        'views/swiftstay_booking_page_template.xml',
        'views/swiftstay_dashboard_template.xml',
        'views/booking_confirmation_email_template.xml',
        'views/website_menu.xml',
        'views/menu.xml',
        
        
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}