from odoo import models, fields, api

class Booking(models.Model):
    _name = 'swiftstay.booking'
    _description = 'Booking Model'
    _rec_name = 'guest_name'

    guest_name = fields.Many2one('res.partner', string="Guest Name", required=True)
    id_no = fields.Integer(string='ID Number')
    passport_no = fields.Char(string='Passport Number')
    email = fields.Char(string='Email Address', required=True)
    phone_no = fields.Integer(string='Phone Number', required=True)
    check_in = fields.Date(string='Check-in Date', required=True)
    check_out = fields.Date(string='Check-out Date', required=True)
    duration = fields.Integer(compute='compute_duration', string='Duration (Days)', store=True)
    room_no = fields.Many2one(
        'swiftstay.rooms', 
        string='Room Number', 
        required=True, 
        domain=[('room_status', '=', 'available')]
    )

    @api.model
    def create(self, vals):
        booking = super(Booking, self).create(vals)
        if booking.room_no:
            booking.room_no.room_status = 'occupied' 
        return booking

    @api.depends('check_in', 'check_out')
    def compute_duration(self):
        for record in self:
            if record.check_in and record.check_out:
                record.duration = (record.check_out - record.check_in).days
            else:
                record.duration = 0
