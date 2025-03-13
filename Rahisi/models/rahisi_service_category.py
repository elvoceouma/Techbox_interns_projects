# -*- coding: utf-8 -*-

from odoo import api, fields, models

class RahisiServiceCategory(models.Model):
    _name = 'rahisi.service.category'
    _description = 'Service Category'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    icon = fields.Binary(string='Icon')
    active = fields.Boolean(string='Active', default=True)
    service_ids = fields.One2many('rahisi.service', 'category_id', string='Services')
    job_count = fields.Integer(string='Job Count', compute='_compute_job_count')

    @api.depends('service_ids.category_id')
    def _compute_job_count(self):
        for record in self:
            record.job_count = self.env['rahisi.job'].search_count([
                ('service_id.category_id', '=', record.id)
            ])
    
    def action_add_service(self):
        """Open form to add a new service to this category"""
        return {
            'name': 'Add Service to Category',
            'type': 'ir.actions.act_window',
            'res_model': 'rahisi.service',
            'view_mode': 'form',
            'context': {
                'default_category_id': self.id,
                'default_provider_id': self.env.context.get('default_provider_id', False),
            },
            'target': 'new',
        }