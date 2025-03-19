from odoo import models, fields

class RentalUnit(models.Model):
    _name = 'rental.unit'
    _description = 'Rental Unit'

    name = fields.Char(string="Unit Name", required=True)
    property_id = fields.Many2one('rental.property', string="Property", required=True)
    tenant_id = fields.Many2one('res.partner', string="Tenant")
    rent_price = fields.Float(string="Rent Price")
    status = fields.Selection([
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Under Maintenance')
    ], string="Status", default="available")