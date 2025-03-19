from odoo import api, fields, models, _

class RahisiServiceProvider(models.Model):
    _name = 'rahisi.service.provider'
    _description = 'Service Provider'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Name', required=True, tracking=True)
    business_name = fields.Char(string='Business Name', tracking=True)
    user_id = fields.Many2one('res.users', string='User', ondelete='restrict', tracking=True)
    address_id = fields.Many2one('res.partner', string='Address', ondelete='restrict', tracking=True)
    services_offered = fields.One2many('rahisi.service', 'provider_id', string='Services Offered')
    rating = fields.Float(string='Rating', compute='_compute_rating', store=True, tracking=True)
    review_count = fields.Integer(string='Review Count', compute='_compute_rating', store=True)
    availability = fields.Selection([
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('unavailable', 'Unavailable')
    ], string='Availability', default='available', tracking=True)
    image = fields.Binary(string='Profile Image', attachment=True)
    phone = fields.Char(string='Phone', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)
    job_ids = fields.One2many('rahisi.job', 'provider_id', string='Jobs')
    review_ids = fields.One2many('rahisi.review', 'provider_id', string='Reviews')
    current_job_id = fields.Many2one('rahisi.job', string='Current Job', compute='_compute_current_job', store=True)

    @api.depends('review_ids', 'review_ids.rating')
    def _compute_rating(self):
        for provider in self:
            reviews = provider.review_ids
            provider.review_count = len(reviews)
            provider.rating = sum(review.rating for review in reviews) / len(reviews) if reviews else 0.0

    @api.depends('job_ids.state', 'job_ids.date')
    def _compute_current_job(self):
        for provider in self:
            current_job = self.env['rahisi.job'].search([
                ('provider_id', '=', provider.id),
                ('state', 'in', ['accepted', 'in_progress'])
            ], limit=1, order='date desc, id desc')
            provider.current_job_id = current_job.id if current_job else False

            # Auto-update availability based on current job
            provider.availability = 'busy' if current_job else 'available'

    @api.model
    def create(self, vals):
        # If user doesn't exist, create one
        if not vals.get('user_id') and vals.get('email'):
            user = self.env['res.users'].create({
                'name': vals.get('name'),
                'login': vals.get('email'),
                'email': vals.get('email'),
                'groups_id': [(6, 0, [self.env.ref('rahisi.group_rahisi_service_provider').id])],
            })
            vals['user_id'] = user.id

        # If address doesn't exist, create one
        if not vals.get('address_id'):
            partner = self.env['res.partner'].create({
                'name': vals.get('name'),
                'phone': vals.get('phone'),
                'email': vals.get('email'),
                'type': 'other',
            })
            vals['address_id'] = partner.id

        return super(RahisiServiceProvider, self).create(vals)
    
    def action_browse_categories(self):
        """Open service categories in kanban view for browsing"""
        return {
            'name': 'Browse Service Categories',
            'type': 'ir.actions.act_window',
            'res_model': 'rahisi.service.category',
            'view_mode': 'kanban,tree',
            'domain': [('active', '=', True)],
            'context': {'default_provider_id': self.id},
            'create': False
        }
    
    def action_add_service(self):
        """Open form to add a new service"""
        return {
            'name': 'Add New Service',
            'type': 'ir.actions.act_window',
            'res_model': 'rahisi.service',
            'view_mode': 'form',
            'context': {'default_provider_id': self.id},
            'target': 'new',
        }