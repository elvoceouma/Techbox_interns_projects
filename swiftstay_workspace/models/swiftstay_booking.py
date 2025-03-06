from odoo import models, fields, api


class Booking(models.Model):
    _name = 'swiftstay.booking'
    _description = 'Booking Model'

    guest_name = fields.Many2one('res.partner', string="Guest Name", required=True)
    id_no = fields.Integer(string='ID Number')
    passport_no = fields.Integer(string='Passport Number', required=True)
    email = fields.Char(string='Email Address', required=True)
    phone_no = fields.Char(string='Phone Number', required=True)
    check_in = fields.Date(string='Check-in Date', required=True)
    check_out = fields.Date(string='Check-out Date', required=True)

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
