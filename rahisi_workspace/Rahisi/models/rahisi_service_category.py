# -*- coding: utf-8 -*-

from odoo import api, fields, models

class RahisiServiceCategory(models.Model):
    _name = 'rahisi.service.category'
    _description = 'Service Category'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    icon = fields.Binary(string='Icon')
    active = fields.Boolean(string='Active', default=True)
    service_ids = fields.One2many('rahisi.service', 'category_id', string='Services')
    job_count = fields.Integer(string='Job Count', compute='_compute_job_count')

    @api.depends()
    def _compute_job_count(self):
        for record in self:
            record.job_count = self.env['rahisi.job'].search_count([
                ('service_id.category_id', '=', record.id)
            ])