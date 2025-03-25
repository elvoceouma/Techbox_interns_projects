from odoo import models, fields

class RentalUnit(models.Model):
    _name = 'rental.unit'
    _description = 'Rental Unit'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Unit Name", required=True, tracking=True)
    property_id = fields.Many2one('rental.property', string="Property", required=True, tracking=True)
    tenant_id = fields.Many2one('res.partner', string="Tenant", tracking=True)
    rental_management_id = fields.Many2one('rental.management', string="Rental Contract", tracking=True)

    rent_price = fields.Float(string="Rent Price", related="rental_management_id.rent_amount", store=True, readonly=True, tracking=True)
    status = fields.Selection([
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Under Maintenance')
    ], string="Status", default="available", tracking=True)
