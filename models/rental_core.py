from odoo import models, fields

class RentalManagement(models.Model):
    _name = 'rental.management'
    _description = 'Rental Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Contract Reference", required=True, tracking=True)
    tenant_id = fields.Many2one('res.partner', string="Tenant", required=True, tracking=True)
    property_id = fields.Many2one('rental.property', string="Property", required=True, tracking=True)
    unit_id = fields.Many2one('rental.unit', string="Rental Unit", required=True, tracking=True)
    start_date = fields.Date(string="Start Date", required=True, tracking=True)
    end_date = fields.Date(string="End Date", required=True, tracking=True)
    rent_amount = fields.Float(string="Rent Amount", required=True, tracking=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('terminated', 'Terminated')
    ], string="Status", default="draft", tracking=True)
