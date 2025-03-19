from odoo import models, fields


class Teacher(models.Model):
    _name = 'teacher.teacher'
    _description = 'Teacher Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'


    name = fields.Char(string='Name', required=True)
    idnumber = fields.Integer(string='ID Number')
    date_of_employment = fields.Date(string='Date of Employment')
    gender = fields.Selection([
        ('Male', 'Male'),
        ('Female', 'Female'),
    ], string= 'Gender')
    gradeteacher = fields.Selection([
        ('Pre-School', 'Pre-School'),
        ('Lower Primary', 'Lower Primary'),
        ('Upper Primary', 'Upper Primary'),
    ], string='Grade', default='Pre-School')
    subjects = fields.Char(string='Subject')
    contact = fields.Integer(string='Contact')
    bank_name = fields.Char(string='Bank Name')
    bank_account = fields.Integer(string='Bank Account')
   


