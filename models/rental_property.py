from odoo import models, fields

class RentalProperty(models.Model):
    _name = 'rental.property'
    _description = 'Rental Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Property Name", required=True, tracking=True)
    address = fields.Text(string="Address", tracking=True)
    owner_id = fields.Many2one('res.partner', string="Owner", tracking=True)
    property_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('commercial', 'Commercial')
    ], string="Property Type", required=True, tracking=True)
    
    rental_units_ids = fields.One2many('rental.unit', 'property_id', string="Rental Units")
