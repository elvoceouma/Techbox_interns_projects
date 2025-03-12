from odoo import models, fields,api

class Rooms(models.Model):
    _name = 'swiftstay.rooms'
    _description = 'Rooms Model'
    _inherit = ['mail.thread']

    name = fields.Char(string='Room Number', required=True, tracking=True)
    room_type_id = fields.Many2one('swiftstay.roomtypes', string='Room Type', required=True, tracking=True) 
    num_beds = fields.Integer(string='Number of Beds', required=True, tracking=True)
    floor_number = fields.Integer(string='Floor Number', required=True, tracking=True)
    room_status = fields.Selection([
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
    ], string='Room Status', default='available', required=True, tracking=True)
    price_per_night = fields.Float(related='room_type_id.price_per_night', string="Price Per Night (Ksh.)", store=True, tracking=True)
    # room_image = fields.Binary(string='Room Image', attachment=True)
    room_image = fields.Image(
    string="Room Image",
    max_width=1024,
    max_height=1024,
    store=True,
    attachment=True, 
    tracking=True
)
    


    def action_occupied(self):
        for room in self:
            room.room_status = 'occupied'
            
    def action_available(self):
        for room in self:
            room.room_status = 'available'
    
    def action_maintenance(self):
        for room in self:
            room.room_status = 'maintenance'