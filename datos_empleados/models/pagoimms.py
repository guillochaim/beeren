from odoo import fields, models

class datosEmpleados (models.Model):
    _inherit = ['mail.activity.plan']
    #Modulo para subir los pagos de imms
    pago_imss = fields.Binary(
        string="Pago de Seguro",
    )

    empresa = fields.Many2one(
        comodel_name='res.company',
        ondelete='set null',
        index=True,
        string="Empresa",
    )

    campo_nones = fields.Char(
        string=".",
    )
