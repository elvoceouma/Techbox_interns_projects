# -*- coding: utf-8 -*-

from odoo import api, fields, models

class RahisiService(models.Model):
    _name = 'rahisi.service'
    _description = 'Service'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    provider_id = fields.Many2one('rahisi.service.provider', string='Service Provider', 
                                 required=True, ondelete='cascade')
    category_id = fields.Many2one('rahisi.service.category', string='Category', 
                                 required=True, ondelete='restrict')
    price = fields.Float(string='Price', required=True)
    description = fields.Text(string='Description')
    portfolio_images = fields.Many2many('ir.attachment', string='Portfolio Images')
    active = fields.Boolean(string='Active', default=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id.id)
    is_available = fields.Boolean(string='Available', compute='_compute_is_available', store=True)

    @api.depends('active', 'provider_id.availability')
    def _compute_is_available(self):
        for service in self:
            service.is_available = service.active and service.provider_id.availability == 'available'
