from odoo import models, fields, api

class RoomTypes(models.Model):
    _name = 'swiftstay.roomtypes'
    _description = 'Room Types Model'
    _inherit = ['mail.thread']

    name = fields.Char(string='Room Type', required=True, tracking=True)
    amenity_ids = fields.Many2many('swiftstay.amenities', string='Amenities', tracking=True)
    room_ids = fields.One2many('swiftstay.rooms', 'room_type_id', string='Rooms')
    price_per_night = fields.Float(string='Price per Night (Ksh.)', required=True, tracking=True)
    roomtype_colour = fields.Integer(string="Colour", required=True, tracking=True)

    has_available_rooms = fields.Boolean(
        string="Has Available Rooms", 
        compute="compute_has_available_rooms", 
        store=True
    )

    @api.depends('room_ids.room_status')
    def compute_has_available_rooms(self):
        for room_type in self:
            room_type.has_available_rooms = any(room.room_status == 'available' for room in room_type.room_ids)
