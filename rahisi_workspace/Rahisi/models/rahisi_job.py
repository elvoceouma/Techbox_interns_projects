# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from math import radians, cos, sin, asin, sqrt

class RahisiJob(models.Model):
    _name = 'rahisi.job'
    _description = 'Job'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, 
                      default=lambda self: _('New'))
    customer_id = fields.Many2one('rahisi.customer', string='Customer', 
                                 required=True, ondelete='restrict', tracking=True)
    provider_id = fields.Many2one('rahisi.service.provider', string='Service Provider', 
                                 required=True, ondelete='restrict', tracking=True)
    service_id = fields.Many2one('rahisi.service', string='Service', 
                               required=True, ondelete='restrict', 
                               domain="[('provider_id', '=', provider_id)]", tracking=True)
    date = fields.Date(string='Date', required=True, tracking=True)
    time = fields.Float(string='Time', tracking=True)
    location_id = fields.Many2one('res.partner', string='Job Location', 
                                 required=True, ondelete='restrict', tracking=True)
    description = fields.Text(string='Description', tracking=True)
    service_price = fields.Float(string='Service Price', related='service_id.price', readonly=True)
    transportation_cost = fields.Float(string='Transportation Cost', compute='_compute_transportation_cost', 
                                      store=True, tracking=True)
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', 
                              store=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    payment_state = fields.Selection([
        ('not_paid', 'Not Paid'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded')
    ], string='Payment Status', default='not_paid', tracking=True)
    review_id = fields.Many2one('rahisi.review', string='Review', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                 default=lambda self: self.env.company.currency_id.id)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('rahisi.job') or _('New')
        
        # Set job location to customer address if not provided
        if not vals.get('location_id') and vals.get('customer_id'):
            customer = self.env['rahisi.customer'].browse(vals.get('customer_id'))
            if customer and customer.address_id:
                vals['location_id'] = customer.address_id.id
        
        # initial state
        if not vals.get('state'):
            vals['state'] = 'requested'
        
        res = super(RahisiJob, self).create(vals)
        # Send notification to provider
        if res.provider_id and res.provider_id.user_id:
            res.message_subscribe(partner_ids=[res.provider_id.user_id.partner_id.id])
            res.message_post(
                body=_("New job request from %s") % res.customer_id.name,
                partner_ids=[res.provider_id.user_id.partner_id.id]
            )
        return res

    @api.depends('provider_id', 'location_id')
    def _compute_transportation_cost(self):
        for job in self:
            if job.provider_id and job.provider_id.address_id and job.location_id:
                # Get transportation config
                config = self.env['rahisi.transportation.config'].search([], limit=1)
                if not config:
                    job.transportation_cost = 0.0
                    continue
            
                # Currently using a simple calculation (as a placeholder)
                distance = self._calculate_distance(
                    job.provider_id.address_id.partner_latitude or 0.0,
                    job.provider_id.address_id.partner_longitude or 0.0,
                    job.location_id.partner_latitude or 0.0,
                    job.location_id.partner_longitude or 0.0
                )
                
                # Calculate cost
                job.transportation_cost = config.base_fee + (distance * config.cost_per_km)
            else:
                job.transportation_cost = 0.0

    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the distance between two points (in kilometers)
        using the Haversine formula
        """
        # This is a placeholder for actual distance calculation
        # Should use Google Maps API
        if not all([lat1, lon1, lat2, lon2]):
            return 5.0  # Default 5km if coordinates not available
        
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers
        return c * r

    @api.depends('service_price', 'transportation_cost')
    def _compute_total_price(self):
        for job in self:
            job.total_price = job.service_price + job.transportation_cost

    def action_request(self):
        self.write({'state': 'requested'})
        # Send notification to provider
        if self.provider_id and self.provider_id.user_id:
            self.message_post(
                body=_("Job request submitted"),
                partner_ids=[self.provider_id.user_id.partner_id.id]
            )
        return True

    def action_accept(self):
        self.write({'state': 'accepted'})
        # Send notification to customer
        if self.customer_id and self.customer_id.user_id:
            self.message_post(
                body=_("Job request accepted by %s") % self.provider_id.name,
                partner_ids=[self.customer_id.user_id.partner_id.id]
            )
        return True

    def action_reject(self):
        self.write({'state': 'rejected'})
        # Send notification to customer
        if self.customer_id and self.customer_id.user_id:
            self.message_post(
                body=_("Job request rejected by %s") % self.provider_id.name,
                partner_ids=[self.customer_id.user_id.partner_id.id]
            )
        return True

    def action_start(self):
        self.write({'state': 'in_progress'})
        # Send notification to customer
        if self.customer_id and self.customer_id.user_id:
            self.message_post(
                body=_("Job started by %s") % self.provider_id.name,
                partner_ids=[self.customer_id.user_id.partner_id.id]
            )
        return True

    def action_complete(self):
        self.write({'state': 'completed'})
        # Send notification to customer
        if self.customer_id and self.customer_id.user_id:
            self.message_post(
                body=_("Job completed by %s. Please provide a review.") % self.provider_id.name,
                partner_ids=[self.customer_id.user_id.partner_id.id]
            )
        return True

    def action_cancel(self):
        if self.state in ['completed', 'cancelled']:
            raise UserError(_("Cannot cancel a completed or already cancelled job."))
        self.write({'state': 'cancelled'})
        # Send notification to both parties
        partners = []
        if self.customer_id and self.customer_id.user_id:
            partners.append(self.customer_id.user_id.partner_id.id)
        if self.provider_id and self.provider_id.user_id:
            partners.append(self.provider_id.user_id.partner_id.id)
        if partners:
            self.message_post(
                body=_("Job has been cancelled"),
                partner_ids=partners
            )
        return True

    def action_create_review(self):
        self.ensure_one()
        if self.state != 'completed':
            raise UserError(_("You can only review completed jobs."))
        if self.review_id:
            raise UserError(_("A review already exists for this job."))
        
        # Create an empty review
        review = self.env['rahisi.review'].create({
            'job_id': self.id,
            'customer_id': self.customer_id.id,
            'provider_id': self.provider_id.id,
            'date': fields.Date.today(),
        })
        
        self.write({'review_id': review.id})
        
        # Open the review form
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'rahisi.review',
            'res_id': review.id,
            'view_mode': 'form',
            'target': 'current',
        }