from odoo import fields, models, api

class FlotaSerrano(models.Model):
    _inherit = "fleet.vehicle"                 
    tipo_vehiculo = fields.Selection([
        ('1','TRACTO CAMION'),
        ('2','TORTON'),
        ('3','PICKUP'),
        ('4','UNIDAD'),
        ('5','MAQUINARIA PESADA'),
        ('6','VOLTEO'),
        ('7','TANQUE'),
        ('8','CAJA SECA'),
        ('9','GONDOLA'),
        ('10','PLATAFORMA'),
        ('11','CAMA BAJA'),
        ('12','CAJA REFRIGERADA'),
        ('13','TANQUE DE ACERO INOXIDABLE'),
        ('14','PLANA'), 
        ('15','REMOLQUE'),
        ('16','TORTON ROLL OFF'),],
        string="Tipo de vehiculo",
    )
    no_economico = fields.Char(
        string="No. economico",
    )   
    capacidad_remolque = fields.Char(
        string="Capacidad Remolque",
    )
    #Parte del motor
    capacidad_tanque =fields.Integer(
        string="Capacidad del Tanque",
    )
    #Parte de modelo
    numero_poliza =fields.Char(
        string="Numero de poliza",
    )
    vigencia_poliza =fields.Date(
        string="Vig. de la poliza",
    ) 
    file_poliza = fields.Binary(
        string="Carga Poliza",
    )
    vigencia_fisico_mecanico =fields.Date(
        string="Vig. Fisico-Mecanico",
    ) 
    file_fisico_mecanico = fields.Binary(
        string="Carga Poliza F-Mecanico",
    )
    vigencia_emisiones =fields.Date(
        string="Vig.Emisiones",
    ) 
    file_emisiones = fields.Binary(
        string="Carga Emisiones",
    )
    file_circulacion = fields.Binary(
        string ="Carga Circulación",
    )
    file_factura = fields.Binary(
        string= "Carga de Factura",
    )
    file_otro = fields.Binary(
        string= "Otro",
    )
    conductor = fields.Many2one(
        comodel_name='hr.employee',
        ondelete='set null',
        index=True,
        string="Conductor",
    )