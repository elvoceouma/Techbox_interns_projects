from odoo import models, fields


class Rental(models.Model):
    _name = 'rental.management'
    _description = 'Rental Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'


    name = fields.Char(string='Tenant Name', required=True)
    house_number = fields.Char(string='House Number')
    house_type = fields.Selection([
        ('bedsitter', 'Bedsitter'),
        ('one_bedroom', 'One Bedroom'),
        ('two_bedroom', 'Two Bedroom'),
    ], string='House Type', default='bedsitter')
    email = fields.Char(string='Email')
    phone_number = fields.Char(string='Phone Number')
    Rent_amount = fields.Float(string='Rent Amount')
    date = fields.Date(string='Date Due')