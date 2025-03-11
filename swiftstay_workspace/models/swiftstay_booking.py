from odoo import models, fields, api

class Booking(models.Model):
    _name = 'swiftstay.booking'
    _description = 'Booking Model'
    _rec_name = 'guest_name'

    guest_name = fields.Many2one('res.partner', string="Guest Name", required=True)
    id_no = fields.Integer(string='ID Number')
    passport_no = fields.Char(string='Passport Number')
    email = fields.Char(string='Email Address', compute="compute_email", readonly=True)
    phone_no = fields.Char(string='Phone Number', compute="compute_phone_number", readonly=True)
    check_in = fields.Date(string='Check-in Date', required=True)
    check_out = fields.Date(string='Check-out Date', required=True)
    duration = fields.Integer(compute='compute_duration', string='Duration (Days)', store=True)
    name = fields.Many2one('swiftstay.roomtypes', string="Room Type")
    room_no = fields.Many2one(
        'swiftstay.rooms', 
        string='Room Number', 
        required=True,
        domain="[('room_status', '=', 'available'), ('room_type_id', '=', name)]"
    )

    price_per_night = fields.Float(related='room_no.price_per_night', string="Price Per Night (Ksh.)", store=True)
    is_checked_out = fields.Boolean(string='Checked Out?', default=False)

    
    
    @api.depends('guest_name')
    def compute_email(self):
        for rec in self:
            if rec.guest_name:
                
                rec.email = rec.guest_name.email
            else:
                rec.email = False
                
    @api.depends('guest_name')
    def compute_phone_number(self):
        for rec in self:
            if rec.guest_name:
             
                rec.phone_no = rec.guest_name.mobile
            else:
                rec.phone_no = False

    @api.model
    def create(self, vals):
        booking = super(Booking, self).create(vals)
        if booking.room_no:
            booking.room_no.room_status = 'occupied' 
        return booking
    
    def write(self, vals):
        res = super(Booking, self).write(vals)
        for booking in self:
            if 'is_checked_out' in vals and vals['is_checked_out']:
                booking.room_no.room_status = 'available'
            else:
                booking.room_no.room_status = 'occupied'
        return res

    @api.depends('check_in', 'check_out')
    def compute_duration(self):
        for record in self:
            if record.check_in and record.check_out:
                record.duration = (record.check_out - record.check_in).days
            else:
                record.duration = 0
    
    


