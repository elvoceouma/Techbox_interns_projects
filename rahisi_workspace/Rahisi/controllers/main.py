from odoo import http, _
from odoo.http import request
from odoo.addons.website.controllers.main import WebsiteController

class RahisiController(WebsiteController):
    
    @http.route('/rahisi/categories', type='http', auth='user', website=True)
    def categories(self, **kw):
        categories = request.env['rahisi.service.category'].search([('active', '=', True)])
        values = {
            'categories': categories,
            'page_name': 'categories',
        }
        return request.render('rahisi.categories_template', values)
    
    @http.route('/rahisi/category/<model("rahisi.service.category"):category>', type='http', auth='user', website=True)
    def category_services(self, category, **kw):
        services = request.env['rahisi.service'].search([
            ('category_id', '=', category.id),
            ('active', '=', True),
            ('is_available', '=', True)
        ])
        values = {
            'category': category,
            'services': services,
            'page_name': 'category_services',
        }
        return request.render('rahisi.category_services_template', values)
        
    @http.route('/rahisi/service/<model("rahisi.service"):service>', type='http', auth='user', website=True)
    def service_details(self, service, **kw):
        values = {
            'service': service,
            'provider': service.provider_id,
            'page_name': 'service_details',
        }
        return request.render('rahisi.service_details_template', values)
        
    @http.route('/rahisi/book/<model("rahisi.service"):service>', type='http', auth='user', website=True)
    def book_service(self, service, **kw):
        # Check again if service is available
        if not service.is_available:
            return request.redirect('/rahisi/categories')
            
        customer = request.env['rahisi.customer'].search([
            ('user_id', '=', request.env.user.id)
        ], limit=1)
        
        if not customer:
            return request.redirect('/rahisi/profile/create')
            
        values = {
            'service': service,
            'provider': service.provider_id,
            'customer': customer,
            'page_name': 'book_service',
        }
        return request.render('rahisi.book_service_template', values)
    
    @http.route('/rahisi/book/confirm', type='http', auth='user', website=True, methods=['POST'], csrf=True)
    def confirm_booking(self, **post):
        service_id = int(post.get('service_id', 0))
        date = post.get('date')
        time = float(post.get('time', 0))
        description = post.get('description', '')
        
        service = request.env['rahisi.service'].browse(service_id)
        customer = request.env['rahisi.customer'].search([
            ('user_id', '=', request.env.user.id)
        ], limit=1)
        
        # Final availability check
        if not service.exists() or not service.is_available:
            return request.redirect('/rahisi/categories')
        
        # Create job request
        job = request.env['rahisi.job'].sudo().create({
            'customer_id': customer.id,
            'provider_id': service.provider_id.id,
            'service_id': service.id,
            'date': date,
            'time': time,
            'location_id': customer.address_id.id,
            'description': description,
            'state': 'requested',
        })
        
        return request.redirect(f'/rahisi/job/{job.id}')
    
    @http.route('/rahisi/provider/dashboard', type='http', auth='user', website=True)
    def provider_dashboard(self, **kw):
        provider = request.env['rahisi.service.provider'].search([
            ('user_id', '=', request.env.user.id)
        ], limit=1)
    
        if not provider:
            return request.redirect('/rahisi/provider/profile/create')
    
        # Get job requests
        requested_jobs = request.env['rahisi.job'].search([
            ('provider_id', '=', provider.id),
            ('state', '=', 'requested')
        ], order='date asc')
    
        # Get active job
        active_jobs = request.env['rahisi.job'].search([
            ('provider_id', '=', provider.id),
            ('state', 'in', ['accepted', 'in_progress'])
        ], order='date asc')
    
        # Get completed jobs
        completed_jobs = request.env['rahisi.job'].search([
            ('provider_id', '=', provider.id),
            ('state', '=', 'completed')
        ], order='date desc', limit=10)
    
        values = {
            'provider': provider,
            'requested_jobs': requested_jobs,
            'active_jobs': active_jobs,
            'completed_jobs': completed_jobs,
            'page_name': 'provider_dashboard',
        }
        return request.render('rahisi.provider_dashboard_template', values)