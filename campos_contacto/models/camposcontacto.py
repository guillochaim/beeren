from odoo import fields, models

class camposcontacto (models.Model):
    _inherit="res.partner"
    #Documentacion personal

    numero_generador_c = fields.Char(
        string="Numero Manifiestos",
    )   
    nombre_representante_c = fields.Char(
        string="Nombre Representante",
    )   

    contacto_firma = fields.Binary(
        string="Firma",
    )

#    numero_generador_c1 = fields.Char(
#        string="Numero Generador",
#    )   