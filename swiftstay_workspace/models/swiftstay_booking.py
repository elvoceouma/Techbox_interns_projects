from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Booking(models.Model):
    _name = 'swiftstay.booking'
    _description = 'Booking Model'
    _rec_name = 'guest_name'
    _inherit = ['mail.thread']

    guest_name = fields.Many2one('res.partner', string="Guest Name", required=True, tracking=True)
    id_no = fields.Char(string='ID Number', size=8, tracking=True) 
    passport_no = fields.Char(string='Passport Number', size=9, tracking=True)
    email = fields.Char(string='Email Address', compute="compute_email", readonly=True)
    phone_no = fields.Char(string='Phone Number', compute="compute_phone_number", readonly=True)
    check_in = fields.Datetime(string='Check-in Date', required=True, tracking=True)
    check_out = fields.Datetime(string='Check-out Date', required=True, tracking=True)
    duration = fields.Integer(string='Duration (Days)', compute='compute_duration', store=True)
    no_of_guests = fields.Integer('Number of Guests', tracking=True)
    name = fields.Many2many('swiftstay.roomtypes', string="Room Types", tracking=True)  
    room_no = fields.Many2many(
        'swiftstay.rooms', 
        string='Room Number', 
        required=True,
        tracking=True,
        domain="[('room_status', '=', 'available'), ('room_type_id', '=', name)]"
    )
    price_per_night = fields.Float(string="Total Price Per Night (Ksh.)", compute="compute_total_price_per_night", store=True)
    total_price = fields.Float(string="Total Price (Ksh.)", compute="compute_total_price", store=True)

    state = fields.Selection([
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('checked_out', 'Checked Out')
    ], string='State', default="available") 

  

    @api.depends('guest_name')
    def compute_email(self):
        for rec in self:
            rec.email = rec.guest_name.email if rec.guest_name else False

    @api.depends('guest_name')
    def compute_phone_number(self):
        for rec in self:
            rec.phone_no = rec.guest_name.mobile if rec.guest_name else False

    @api.depends('check_in', 'check_out')
    def compute_duration(self):
        for record in self:
            if record.check_in and record.check_out:
                record.duration = (record.check_out - record.check_in).days
            else:
                record.duration = 0

    @api.depends('room_no')
    def compute_total_price_per_night(self):
        for record in self:
            record.price_per_night = sum(record.room_no.mapped('price_per_night'))
    
    @api.depends('price_per_night')
    def compute_total_price(self):
        for record in self:
            record.total_price = record.duration * record.price_per_night
    
    @api.model
    def create(self, vals):
        booking = super(Booking, self).create(vals)

        if 'room_no' in vals and booking.room_no:
            booking.room_no.write({'room_status': 'occupied'})
        booking.state = 'occupied'

       
        invoice_lines = [
            (0, 0, {
                'product_id': room.name.id,
                'name': room.room_type_id.name,  
                'quantity': booking.duration,
                'price_unit': room.price_per_night
            })
            for room in booking.room_no if room.name
        ]

        if invoice_lines:
            self.env['account.move'].create({
                'partner_id': booking.guest_name.id,
                'move_type': 'out_invoice',
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': invoice_lines
            })

        return booking



    def action_confirm(self):
        for booking in self:
            booking.write({'state': 'checked_out'})

          
            if booking.room_no:
                booking.room_no.write({'room_status': 'available'})

                