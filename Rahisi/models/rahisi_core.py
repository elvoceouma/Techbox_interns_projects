# -*- coding: utf-8 -*-

from odoo import api, fields, models

class RahisiDashboard(models.Model):
    _name = 'rahisi.dashboard'
    _description = 'Rahisi Dashboard'

    name = fields.Char(default='Dashboard')
    total_providers = fields.Integer(compute='_compute_dashboard_data', store=True)
    total_customers = fields.Integer(compute='_compute_dashboard_data', store=True)
    active_jobs = fields.Integer(compute='_compute_dashboard_data', store=True)
    completed_jobs = fields.Integer(compute='_compute_dashboard_data', store=True)
    
   #date field
    last_update = fields.Datetime(string='Last Updated', default=fields.Datetime.now)

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
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'rahisi.dashboard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
            'flags': {'form': {'action_buttons': True}}
        }