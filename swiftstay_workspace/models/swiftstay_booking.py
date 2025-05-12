from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import pytz
import os
from twilio.rest import Client


_logger = logging.getLogger(__name__)

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
    no_of_guests = fields.Integer('Number of Guests', tracking=True, default=1)
    name = fields.Many2many(
    'swiftstay.roomtypes', 
    string="Room Types", 
    tracking=True,
    domain="[('has_available_rooms', '=', True)]"
)
 
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
        ('reserved_by_admin', 'Reserved By Admin'),
        ('reserved_by_guest','Reserved By Guest'),
        ('checked_out', 'Checked Out')
    ], string='State', default="available") 
    
    
    check_in_eat = fields.Datetime(string='Check-in (EAT)', compute="compute_eat_times", store=True)
    check_out_eat = fields.Datetime(string='Check-out (EAT)', compute="compute_eat_times", store=True)

    @api.depends('check_in', 'check_out')
    def compute_eat_times(self):
        EAT = pytz.timezone('Africa/Nairobi')

        for record in self:
            if record.check_in:
                check_in_eat = record.check_in.replace(tzinfo=pytz.utc).astimezone(EAT)
            record.check_in_eat = check_in_eat.replace(tzinfo=None)
            if record.check_out:
                check_out_eat = record.check_out.replace(tzinfo=pytz.utc).astimezone(EAT)
            record.check_out_eat = check_out_eat.replace(tzinfo=None)


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

        
        is_admin_or_officer = self.env.user.has_group('swiftstay_workspace.group_swiftstay_admin') or \
                            self.env.user.has_group('swiftstay_workspace.group_swiftstay_officer')

        if 'room_no' in vals and booking.room_no:
            booking.room_no.write({'room_status': 'occupied'})

        if is_admin_or_officer:
            booking.state = 'reserved_by_admin'
        else:
            booking.state = 'reserved_by_guest'  

       
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

      
        try:
            email_template = self.env.ref('swiftstay_workspace.booking_confirmation_email_template')
            if email_template and booking.guest_name.email:
                email_template.sudo().write({'email_to': booking.guest_name.email})
                _logger.info(f"Booking Email: {booking.guest_name.email}")
                email_template.sudo().send_mail(booking.id, force_send=True)
                _logger.info("Email sent successfully!")
        except Exception as e:
            _logger.error("Failed to send email: %s", e)
            raise UserError("There was an issue sending the booking confirmation email.")
        
        
        try:
            if booking.phone_no:
                twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
                twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
                twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

               
                

                client = Client(twilio_sid, twilio_auth_token)
                room_numbers = ", ".join(booking.room_no.mapped('name.name'))
                message_body = f"Dear {booking.guest_name.name}, your booking at SwiftStay is confirmed from {booking.check_in_eat} to {booking.check_out_eat}. Room(s): {room_numbers}. Thank you!"

              

                message = client.messages.create(
                    body=message_body,
                    from_=twilio_phone_number,
                    to=booking.phone_no
                )
                
                message_status = client.messages(message.sid).fetch()
                print(f"Message Status: {message_status.status}")
                print(f"Message Status: {message.status}")
                print(f"Error Code: {message.error_code}")

                _logger.info(f"SMS sent successfully! SID: {message.sid}")
        except Exception as e:
            _logger.error("Error while sending SMS: %s", e)
            raise UserError("There was an issue sending the booking confirmation SMS.")
        return booking
    

        
     



    def action_confirm(self):
        for booking in self:
            booking.write({'state': 'checked_out'})

          
            if booking.room_no:
                booking.room_no.write({'room_status': 'available'})

                