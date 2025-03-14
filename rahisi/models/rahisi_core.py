# -*- coding: utf-8 -*-

from odoo import api, fields, models

class RahisiDashboard(models.Model):
    _name = 'rahisi.dashboard'
    _description = 'Rahisi Dashboard'
    _rec_name = 'name'

    name = fields.Char(default='Dashboard', readonly=True)
    total_providers = fields.Integer(compute='_compute_dashboard_data')
    total_customers = fields.Integer(compute='_compute_dashboard_data')
    active_jobs = fields.Integer(compute='_compute_dashboard_data')
    completed_jobs = fields.Integer(compute='_compute_dashboard_data')
    
    # date field
    last_update = fields.Datetime(string='Last Updated', default=fields.Datetime.now)

    # Prevent creating multiple dashboard records
    @api.model
    def create(self, vals):
        if self.search_count([]) >= 1:
            return self.search([], limit=1)
        return super(RahisiDashboard, self).create(vals)

    @api.depends('last_update')
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

    def refresh_dashboard(self):
        """Refresh the dashboard data"""
        self.last_update = fields.Datetime.now()
        return True