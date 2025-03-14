from odoo import models, fields, api
import logging


class Rooms(models.Model):
    _name = 'swiftstay.rooms'
    _description = 'Rooms Model'
    _inherit = ['mail.thread']
    

    name = fields.Many2one('product.product', string="Room Number", tracking=True)

    room_type_id = fields.Many2one('swiftstay.roomtypes', string='Room Type', required=True, tracking=True) 
    num_beds = fields.Integer(string='Number of Beds', required=True, tracking=True)
    floor_number = fields.Integer(string='Floor Number', required=True, tracking=True)
    room_status = fields.Selection([
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
    ], string='Room Status', default='available', required=True, tracking=True)
    price_per_night = fields.Float(related='room_type_id.price_per_night', string="Price Per Night (Ksh.)", store=True, tracking=True)

    room_image = fields.Binary(
        string="Room Image",
        attachment=True,
        related='name.image_1920', 
        tracking=True
    )
    

    room_colour = fields.Integer(string="Colour", required=True, tracking=True)

    @api.depends('name')
    def compute_display_name(self):
        for record in self:
            record.display_name = record.name.name if record.name else "Unnamed Room"

    def action_occupied(self):
        for room in self:
            room.room_status = 'occupied'
            
    def action_available(self):
        for room in self:
            room.room_status = 'available'
    
    def action_maintenance(self):
        for room in self:
            room.room_status = 'maintenance'
    
 
    
 