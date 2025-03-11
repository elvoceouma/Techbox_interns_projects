# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class RahisiTransportationConfig(models.Model):
    _name = 'rahisi.transportation.config'
    _description = 'Transportation Cost Configuration'

    name = fields.Char(string='Name', required=True)
    cost_per_km = fields.Float(string='Cost per Kilometer', required=True, default=1.0)
    base_fee = fields.Float(string='Base Fee', required=True, default=5.0)
    active = fields.Boolean(string='Active', default=True)

    @api.constrains('cost_per_km', 'base_fee')
    def _check_values(self):
        for config in self:
            if config.cost_per_km < 0:
                raise ValidationError(_("Cost per kilometer cannot be negative."))
            if config.base_fee < 0:
                raise ValidationError(_("Base fee cannot be negative."))