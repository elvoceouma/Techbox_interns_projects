from odoo import models, fields

class RoomTypes(models.Model):
    _name = 'swiftstay.roomtypes'
    _description = 'Room Types Model'
    _inherit = ['mail.thread']

    name = fields.Char(string='Room Type', required=True, tracking=True) 
    amenity_ids = fields.Many2many('swiftstay.amenities', string='Amenities', tracking=True)
    room_ids = fields.One2many('swiftstay.rooms', 'room_type_id', string='Rooms')
    price_per_night = fields.Float(string='Price per Night (Ksh.)', required=True, tracking=True)
