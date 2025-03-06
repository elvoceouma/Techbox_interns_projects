from odoo import models, fields

class RoomTypes(models.Model):
    _name = 'swiftstay.roomtypes'
    _description = 'Room Types Model'

    name = fields.Char(string='Room Type', required=True) 
    amenity_ids = fields.Many2many('swiftstay.amenities', string='Amenities')
    room_ids = fields.One2many('swiftstay.rooms', 'room_type_id', string='Rooms')
