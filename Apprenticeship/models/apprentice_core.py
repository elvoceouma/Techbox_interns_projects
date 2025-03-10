from odoo import models, fields


class Apprentice(models.Model):
    _name = 'apprentice.apprentice'
    _description = 'Apprentice Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'


    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    level = fields.Selection([
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ], string='Level', default='beginner')
    email = fields.Char(string='Email')
    amount = fields.Float(string='Amount')
    date = fields.Date(string='Date of registration')