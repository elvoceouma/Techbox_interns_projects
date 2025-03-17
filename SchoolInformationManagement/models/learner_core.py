from odoo import models, fields


class Learner(models.Model):
    _name = 'learner.learner'
    _description = 'Learner Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'


    name = fields.Char(string='Name', required=True)
    number = fields.Char(string='Admission Number')
    date = fields.Date(string='Date of Birth')
    gender = fields.Selection([
        ('Male', 'Male'),
        ('Female', 'Female'),
    ], string= 'Gender')
    grade = fields.Selection([
        ('Pre-School', 'Pre-School'),
        ('Lower Primary', 'Lower Primary'),
        ('Upper Primary', 'Upper Primary'),
    ], string='Grade', default='Pre-School')
    pname = fields.Char(string='Parent Name')
    contact = fields.Float(string='Contact')
    route = fields.Char(string='Route')


