from odoo import models, fields

class Amenities(models.Model):
    _name = 'swiftstay.amenities'
    _description = 'Amenities Model'

    name = fields.Char(string='Amenity Name', required=True)
