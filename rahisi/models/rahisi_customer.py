# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class RahisiCustomer(models.Model):
    _name = 'rahisi.customer'
    _description = 'Customer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Name', required=True, tracking=True)
    user_id = fields.Many2one('res.users', string='User', ondelete='restrict', tracking=True)
    address_id = fields.Many2one('res.partner', string='Address', ondelete='restrict', tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    job_history = fields.One2many('rahisi.job', 'customer_id', string='Job History')
    active = fields.Boolean(string='Active', default=True, tracking=True)

    @api.model
    def create(self, vals):
       
        if not vals.get('address_id'):
            partner = self.env['res.partner'].create({
                'name': vals.get('name'),
                'phone': vals.get('phone'),
                'email': vals.get('email'),
                'type': 'other'
            })
            vals['address_id'] = partner.id

        return super(RahisiCustomer, self).create(vals)