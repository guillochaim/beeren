from odoo import fields, models

class datosEmpleados (models.Model):
    _inherit="hr.employee"
    #Documentacion personal
    acta_nacimiento = fields.Binary(
        string="Acta de Nacimiento",
        groups="hr.group_hr_user",
    )
    domicilio = fields.Binary(
        string="Comp. Domicilio",
        groups="hr.group_hr_user",
    )
    estudios = fields.Binary(
        string="Comp. Estudios",
        groups="hr.group_hr_user",
    )
    curp_serra = fields.Binary(
        string="CURP Empleado",
        groups="hr.group_hr_user",
    )
    rfc_serra = fields.Binary(
        string="RFC Empleado",
        groups="hr.group_hr_user",
    )
    ine = fields.Binary(
        string="INE",
        groups="hr.group_hr_user",
    )
    #Seguro
    nseguridad_social_serra = fields.Char(
        string="NSS Empleado",
        groups="hr.group_hr_user",
    )
    alta_patronal = fields.Date(
        string="Fecha de alta patronal",
        groups="hr.group_hr_user",
    )
    alta_imss = fields.Binary(
        string="Alta IMSS",
        groups="hr.group_hr_user",
    )
    infonavit = fields.Binary(
        string="Comp. Infonavit",
        groups="hr.group_hr_user",
    )
    #Contratos
    empleado_fecha_ingreso = fields.Date(
        string="Fecha de ingreso",
        groups="hr.group_hr_user",
    )
    empleado_contrato = fields.Binary(
        string="Contrato",
        groups="hr.group_hr_user",
    )
    empleado_reglamento = fields.Binary(
        string="Reglamento",
        groups="hr.group_hr_user",
    )
    empleado_codigo_etica = fields.Binary(
        string="Codigo Etica",
        groups="hr.group_hr_user",
    )
    empleado_baja_fecha = fields.Date(    
        string="Fecha Baja",
        groups="hr.group_hr_user",
    )
    empleado_baja = fields.Binary(
        string="Baja",
        groups="hr.group_hr_user",
    )
    empleado_motivo_baja = fields.Text(
        string="Motivo",
        groups="hr.group_hr_user",
    )  
    no_antesedentes = fields.Binary(
        string="Carta Antecedentes",
        groups="hr.group_hr_user",
    )   
    recomendacion1 = fields.Binary(
        string="Carta de recomendación 1",
        groups="hr.group_hr_user",
    )
    recomendacion2 = fields.Binary(
        string="Carta de recomendación 2",
        groups="hr.group_hr_user",
    )
    #Vehiculo
    licencia = fields.Binary(
        string="Licencia",
        groups="hr.group_hr_user",
    )
    licencia_1 = fields.Text(
        string="Numero de Licencia",
        groups="hr.group_hr_user",
    )
    vigencia = fields.Date(
        string="Vigencia",
        groups="hr.group_hr_user",
    )
    chofer_examen = fields.Binary(
        string="Examen de manejo",
        groups="hr.group_hr_user",
    )
    vigencia_exam = fields.Date(
        string="Vigencia Examen",
        groups="hr.group_hr_user",
    )
    #responsivas
    res_unidad = fields.Binary(
        string="Unidad",
        groups="hr.group_hr_user",
    )
    res_llave_caseta = fields.Binary(
        string="Llave caseta",
        groups="hr.group_hr_user",
    )
    res_llave_diesel = fields.Binary(
        string="Llave Diesel",
        groups="hr.group_hr_user",
    )
    res_telefono = fields.Binary(
        string="Telefono",
        groups="hr.group_hr_user",
    )
    res_equipo = fields.Binary(
        string="Equipo",
        groups="hr.group_hr_user",
    )
    res_resguardo1 = fields.Binary(
        string="Resguardo 1",
        groups="hr.group_hr_user",
    )
    res_resguardo2 = fields.Binary(
        string="Resguardo 2",
        groups="hr.group_hr_user",
    )

    #Fernando Marzo 2023
    f_rcontrol = fields.Binary(
        string="R Control",
        groups="hr.group_hr_user",
    )

    f_pasaporte = fields.Binary(
        string="Pasaporte",
        groups="hr.group_hr_user",
    )

    f_fpasaporte = fields.Date(
        string="Vigencia Pasaporte",
        groups="hr.group_hr_user",
    )

    f_visa = fields.Binary(
        string="Visa",
        groups="hr.group_hr_user",
    )

    f_fvisa = fields.Date(
        string="Vigencia Visa",
        groups="hr.group_hr_user",
    )

    f_afore = fields.Binary(
        string="Afore",
        groups="hr.group_hr_user",
    )

    #Fernando Marzo 2024
    f_firma = fields.Binary(
        string="Firma",
        groups="hr.group_hr_user",
    )