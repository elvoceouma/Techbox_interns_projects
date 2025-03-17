from odoo import models, fields


class Subjects(models.Model):
    _name = 'subjects.subjects'
    _description = 'Subjects Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'


    name = fields.Char(string='Subject Name', required=True)
    level= fields.Selection([
        ('Pre-School', 'Pre-School'),
        ('Lower Primary', 'Lower Primary'),
        ('Upper Primary', 'Upper Primary'),
    ], string='Grade', default='Pre-School')
    teacher = fields.Char(string='Teacher')
    grade = fields.Integer(string='Grade')
    learner = fields.Char(string='Learners Name')
   
   


