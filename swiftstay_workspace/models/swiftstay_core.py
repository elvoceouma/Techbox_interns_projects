from odoo import models, fields


class SwiftStay(models.Model):
    _name = 'swiftstay.swiftstay'
    _description = 'SwiftStay Model'
   


    room_no = fields.Char(string='Room Number', required=True)
    no_of_beds = fields.Integer('Number of  Beds')
    availability = fields.Boolean('Room Availability', required=True, default= False)
    
    
    
    
