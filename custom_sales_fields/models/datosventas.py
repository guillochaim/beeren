from odoo import fields, models

class clientescampos (models.Model):
    _inherit="sale.order"
    #Documentacion personal

    contact_id = fields.Many2one('res.partner', string='Contacto Interno', readonly=False,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=False, domain="[('type', '!=', 'private'), ('company_id', 'in', (False, company_id))]",)   