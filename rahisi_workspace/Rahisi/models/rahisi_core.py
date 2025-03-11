# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class RahisiDashboard(models.TransientModel):
    _name = 'rahisi.dashboard'
    _description = 'Rahisi Dashboard'

    name = fields.Char(default='Dashboard')
    total_providers = fields.Integer(compute='_compute_dashboard_data')
    total_customers = fields.Integer(compute='_compute_dashboard_data')
    active_jobs = fields.Integer(compute='_compute_dashboard_data')
    completed_jobs = fields.Integer(compute='_compute_dashboard_data')
    recent_jobs = fields.Many2many('rahisi.job', compute='_compute_dashboard_data')
    top_providers = fields.Many2many('rahisi.service.provider', compute='_compute_dashboard_data')
    popular_categories = fields.Many2many('rahisi.service.category', compute='_compute_dashboard_data')

    @api.depends()
    def _compute_dashboard_data(self):
        for record in self:
            # Count providers and customers
            record.total_providers = self.env['rahisi.service.provider'].search_count([('active', '=', True)])
            record.total_customers = self.env['rahisi.customer'].search_count([('active', '=', True)])
            
            # Count jobs
            record.active_jobs = self.env['rahisi.job'].search_count([
                ('state', 'in', ['requested', 'accepted', 'in_progress'])
            ])
            record.completed_jobs = self.env['rahisi.job'].search_count([('state', '=', 'completed')])
            
            # Get recent jobs
            record.recent_jobs = self.env['rahisi.job'].search([
                ('state', 'not in', ['cancelled', 'rejected'])
            ], limit=10, order='create_date desc')
            
            # Get top rated providers
            record.top_providers = self.env['rahisi.service.provider'].search([
                ('active', '=', True),
                ('rating', '>', 0)
            ], limit=5, order='rating desc, review_count desc')
            
            # Get popular categories
            # First, compute job count per category
            categories = self.env['rahisi.service.category'].search([('active', '=', True)])
            category_data = []
            for category in categories:
                job_count = self.env['rahisi.job'].search_count([
                    ('service_id.category_id', '=', category.id)
                ])
                category_data.append((category, job_count))
            
            # Sort by job count and take top 5
            category_data.sort(key=lambda x: x[1], reverse=True)
            record.popular_categories = self.env['rahisi.service.category'].browse([
                c[0].id for c in category_data[:5]
            ])