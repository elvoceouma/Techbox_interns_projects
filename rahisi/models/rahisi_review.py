# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class RahisiReview(models.Model):
    _name = 'rahisi.review'
    _description = 'Review'
    _order = 'date desc, id desc'

    job_id = fields.Many2one('rahisi.job', string='Job', required=True, ondelete='cascade')
    customer_id = fields.Many2one('rahisi.customer', string='Customer', required=True, 
                                 ondelete='restrict')
    provider_id = fields.Many2one('rahisi.service.provider', string='Service Provider', 
                                 required=True, ondelete='restrict')
    rating = fields.Float(string='Rating', required=True, default=5.0)
    comment = fields.Text(string='Comment')
    date = fields.Date(string='Date', default=fields.Date.today, required=True)

    @api.constrains('rating')
    def _check_rating(self):
        for review in self:
            if review.rating < 1.0 or review.rating > 5.0:
                raise ValidationError(_("Rating must be between 1 and 5."))

    @api.model
    def create(self, vals):
        res = super(RahisiReview, self).create(vals)
        # Recalculate provider rating
        if res.provider_id:
            res.provider_id._compute_rating()
        # Notify the provider
        if res.provider_id and res.provider_id.user_id:
            res.job_id.message_post(
                body=_("A review has been added by %s with rating %.1f") % (res.customer_id.name, res.rating),
                partner_ids=[res.provider_id.user_id.partner_id.id]
            )
        return res

    def write(self, vals):
        res = super(RahisiReview, self).write(vals)
        # Recalculate provider rating if rating changes
        if 'rating' in vals:
            for review in self:
                if review.provider_id:
                    review.provider_id._compute_rating()
        return res