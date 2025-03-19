from odoo import models, fields

class RentalProperty(models.Model):
    _name = 'rental.property'
    _description = 'Rental Property'

    name = fields.Char(string="Property Name", required=True)
    address = fields.Text(string="Address")
    owner_id = fields.Many2one('res.partner', string="Owner")
    property_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('commercial', 'Commercial')
    ], string="Property Type", required=True)
    rental_units_ids = fields.One2many('rental.unit', 'property_id', string="Rental Units")
