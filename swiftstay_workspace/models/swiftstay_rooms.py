from odoo import models, fields

class Rooms(models.Model):
    _name = 'swiftstay.rooms'
    _description = 'Rooms Model'

    name = fields.Integer(string='Room Number', required=True)
    room_type_id = fields.Many2one('swiftstay.roomtypes', string='Room Type', required=True) 
    num_beds = fields.Integer(string='Number of Beds', required=True)
    floor_number = fields.Integer(string='Floor Number', required=True)
    room_status = fields.Selection([
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
    ], string='Room Status', default='available', required=True)
    price_per_night = fields.Float(related='room_type_id.price_per_night', string="Price Per Night (Ksh.)", store=True)
    room_image = fields.Binary(string='Room Image')
  
