from odoo import models, fields


class Parents(models.Model):
    _name = 'parents.parents'
    _description = 'Parents Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'


    name = fields.Char(string='Name', required=True)
    idnumber = fields.Integer(string='ID Number')
    childname = fields.Char(string='Child Name', required=True)
    grade = fields.Selection([
        ('Pre-School', 'Pre-School'),
        ('Lower Primary', 'Lower Primary'),
        ('Upper Primary', 'Upper Primary'),
    ], string='Grade', default='Pre-School')
    contact = fields.Integer(string='Contact')
   


