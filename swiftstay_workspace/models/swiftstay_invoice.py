from odoo import models, fields, api

class Invoice(models.Model):
    _name = 'swiftstay.invoice'
    _description = 'Invoice Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    booking_id = fields.Many2one('swiftstay.booking', string='Guest Name', required=True, tracking=True)
    id_no = fields.Integer(related='booking_id.id_no', string="ID Number", store=True, tracking=True)
    passport_no = fields.Char(related='booking_id.passport_no', string="Passport Number", store=True, tracking=True)
    email = fields.Char(related='booking_id.email', string="Email Address", store=True, tracking=True)
    phone_no = fields.Integer(related='booking_id.phone_no', string="Phone Number", store=True, tracking=True)
    room_id = fields.Many2one(related='booking_id.room_no', string="Room Number", store=True, tracking=True)
    room_type_id = fields.Many2one(related='booking_id.room_no.room_type_id', string="Room Type", store=True, tracking=True)
    check_in = fields.Date(related='booking_id.check_in', string="Check-in Date", store=True, tracking=True)
    check_out = fields.Date(related='booking_id.check_out', string="Check-out Date", store=True, tracking=True)
    duration = fields.Integer(related='booking_id.duration', string="Duration (Days)", store=True, tracking=True)
    price_per_night = fields.Float(related='booking_id.room_no.price_per_night', string="Price per night (Ksh.)", store=True, tracking=True)
    total_amount = fields.Float(string="Total Amount (Ksh.)", compute='compute_total_amount', store=True, tracking=True)
    payment_method = fields.Char(string="Payment Method", required=True)
    status = fields.Selection([
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid')
    ], string='Payment Status', default='unpaid', required=True, tracking=True)
    
    

    @api.depends('booking_id.room_no.price_per_night','booking_id.duration')
    def compute_total_amount(self):
        for record in self:
            if record.booking_id.duration and record.booking_id.room_no:
                record.total_amount = record.booking_id.duration * record.booking_id.room_no.price_per_night

