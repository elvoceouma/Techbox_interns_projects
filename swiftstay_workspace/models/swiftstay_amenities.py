from odoo import models, fields

class Amenities(models.Model):
    _name = 'swiftstay.amenities'
    _description = 'Amenities Model'
    _inherit = ['mail.thread']

    name = fields.Char(string='Amenity Name', required=True, tracking=True)
    colour = fields.Integer(string="Colour", required=True, tracking=True)
