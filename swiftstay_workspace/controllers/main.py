from odoo import http, fields
from odoo.http import request
import logging
from odoo.exceptions import UserError
from datetime import datetime, timedelta
import os
from twilio.rest import Client



_logger = logging.getLogger(__name__)

class RoomController(http.Controller):

    @http.route('/available_rooms', type='http', auth="public", website=True)
    def room_list(self):
        rooms = request.env['swiftstay.rooms'].sudo().search([('room_status', '=', 'available')])
       
        grouped_rooms = {}
        for room in rooms:
            room_type = room.room_type_id.name
            if room_type not in grouped_rooms:
                grouped_rooms[room_type] = []
            grouped_rooms[room_type].append(room)
        return request.render('swiftstay_workspace.room_details', {'grouped_rooms': grouped_rooms})

    @http.route('/room_booking', type='http', auth='public', website=True, csrf=False)
 
    def room_booking(self, **kwargs):
        _logger.info("Room booking kwargs: %s", kwargs)

        user = request.env.user
        guest_name = user.partner_id.name
        email = user.email
        mobile = user.partner_id.mobile  
        room_ids = request.httprequest.form.getlist('room_ids')
        if not room_ids or not all(id.isdigit() for id in room_ids):
            _logger.warning("No valid room selected! Redirecting...")
            return request.redirect('/available_rooms')

        rooms = request.env['swiftstay.rooms'].sudo().browse([int(room_id) for room_id in room_ids])
        total_price = sum(room.price_per_night for room in rooms)
        
        return request.render('swiftstay_workspace.booking_page', {
            'rooms': rooms,
            'total_price': total_price,
            'guest_name': guest_name,
            'email': email,
            'mobile': mobile  
        })



    @http.route('/room_booking/submit', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    
    
    def room_booking_submit(self, **post):
        _logger.info("Room booking submit post: %s", post)
        
        room_ids = request.httprequest.form.getlist('room_ids')
        if not room_ids:
            _logger.warning("No valid room selected! Redirecting...")
            return request.redirect('/available_rooms')

        room_ids = [int(room_id) for room_id in room_ids if room_id.isdigit()]

        guest_name = post.get('guest_name')
        if guest_name != request.env.user.partner_id.name:
            _logger.warning("Guest name does not match the logged-in user's name!")
            raise UserError("The guest name must match your account name.")

     
        partner = request.env['res.partner'].sudo().search([('name', '=', guest_name)], limit=1)
        if not partner:
            partner = request.env['res.partner'].sudo().create({
                'name': guest_name,
                'email': post.get('email'),
                'mobile': post.get('phone_no') 
            })
        else:
            
            if not partner.mobile and post.get('phone_no'):
                partner.write({'mobile': post.get('phone_no')})
        check_in_str = post.get('check_in')
        check_out_str = post.get('check_out')

        if check_in_str and check_out_str:
            try:
                
                formatted_check_in = datetime.fromisoformat(check_in_str)
                formatted_check_out = datetime.fromisoformat(check_out_str)
                check_in = fields.Datetime.from_string(formatted_check_in)
                check_out = fields.Datetime.from_string(formatted_check_out)
                check_in = check_in - timedelta(hours=3)
                check_out = check_out - timedelta(hours=3)
                 
        
                
            except ValueError:
                _logger.warning("Invalid check-in/check-out times!")
                raise UserError("Please provide valid check-in and check-out times.")
        else:
            _logger.warning("Invalid check-in/check-out times!")
            raise UserError("Please provide valid check-in and check-out times.")

        rooms = request.env['swiftstay.rooms'].sudo().browse(room_ids)
        room_type_ids = {room.room_type_id.id for room in rooms}
        booking = request.env['swiftstay.booking'].sudo().create({
            'guest_name': partner.id,
            'phone_no': post.get('phone_no'),
            'email': post.get('email'),
            'id_no': post.get('id_no'),
            'passport_no': post.get('passport_no'),
            'check_in': check_in,
            'check_out': check_out,
            'no_of_guests': post.get('no_of_guests'),
            'name': [(6, 0, room_type_ids)],
            'room_no': [(6, 0, room_ids)],
  
        })
   
        _logger.info("Booking created successfully! Triggering email.")
        values = {  'guest_name': partner.id,
            'phone_no': post.get('phone_no'),
            'email': post.get('email'),
            'id_no': post.get('id_no'),
            'passport_no': post.get('passport_no'),
            'check_in': check_in,
            'check_out': check_out,
            'no_of_guests': post.get('no_of_guests'),
            'room_no': [(6, 0, room_ids)], }
        _logger.info(values)
        
        try:
            email_template = request.env.ref('swiftstay_workspace.booking_confirmation_email_template')
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
               
   
        _logger.info("Redirecting to My Bookings page.")
        return request.redirect('/my_bookings')


    @http.route('/my_bookings', type='http', auth='user', website=True)
    def my_bookings(self):
        user = request.env.user
        bookings = request.env['swiftstay.booking'].sudo().search(
            [('guest_name', '=', user.partner_id.name)], 
            order="create_date desc"  
        )
        
        return request.render('swiftstay_workspace.user_dashboard', {'bookings': bookings})

