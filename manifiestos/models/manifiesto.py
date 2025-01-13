import base64
from io import BytesIO
from PIL import Image
from odoo import models, fields, api
from odoo.exceptions import UserError  # Importar UserError
import logging

_logger = logging.getLogger(__name__)

class Manifiesto(models.Model):
    _name = 'manifiestos.manifiesto'
    _description = 'Manifiesto de residuos'

    name = fields.Char(string='Numero de Manifiesto', compute='_compute_name', store=True)

    sello = fields.Char(string='SELLO: ', required=True)

    create_date = fields.Date(string='Fecha de Creación', readonly=True)

    num_mani = fields.Char(string='Numero de Generador', required=True)

    instrucciones = fields.Char(string='Instrucciones de residuo', required=True)

    observaciones = fields.Text(string='Observaciones generales')

    nombre_7 = fields.Char(string='Nombre y Firma', required=True)

    ruta = fields.Char(string='Ruta de la empresa', required=True)

    partner_id = fields.Many2one('res.partner', string='Cliente')

    f_rcontrol = fields.Binary("Firma de Control")

    firma_id_1= fields.Many2one('sign.request', string='Firma Documento') 
    firma_id_2= fields.Many2one('sign.template', string='Firma Documento Template') 

    firma_state = fields.Char(string='Estado de la Firma', compute='_compute_firma_state')

    firma_url = fields.Char(string='URL de Firma', compute='_compute_firma_url', store=True)

    emp_permiso = fields.Char(string='Numero autorización', compute='_compute_permiso', store=True)

    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehículo')

    fecha_1 = fields.Date(string='Fecha de embarque')

    contact_id = fields.Many2one('res.partner', string='Destino')

    acopio_id = fields.Many2one('res.partner', string='Contacto')

    fecha_2 = fields.Date(string='Fecha de recepción')

    lines = fields.One2many('manifiestos.line', 'manifiesto_id', string='Líneas de facturación')


    chofer_bd_man = fields.Selection([
        ('bd', 'Tralisol'),
        ('man', 'Manual'),
    ], string='Chofer', required=True , default='bd')
    # 25
    # f_firma_chofer = fields.Binary(string="Firma Chofer")

#ok
    # chofer_bd_man_bol = fields.Boolean(string='Chofer Asignado')
    # f_firma_chofer = fields.Binary(string='Firma del Chofer')

    #Campos sin permisos 
    # 25
    # conductor_firma = fields.Char(string='Firma del Conductor', compute='_compute_conductor_firma')


    # @api.depends('vehicle_id.conductor')
    # def _compute_conductor_firma(self):
    #     for record in self:
    #         # Usar sudo para evitar problemas de permisos
    #         conductor = record.vehicle_id.conductor.sudo()
    #         record.conductor_firma = conductor.f_firma if conductor else ''
    # 25
#Campos sin permisos 

    def generate_qr_code_text(self):
        #Datos de tralisol directos
        # emp_tralisol_display = self.emp_tralisol.upper() if self.emp_tralisol else ''
        emp_tralisol_display = 'TRANSPORTADORA TRALISOL, CARRETERA AL PUESTO KM6, CENTRO, LAGOS DE MORENO, JALISCO. MEXICO CP 47400'

        fecha_2_upper = self.fecha_2.upper() if isinstance(self.fecha_2, str) else self.fecha_2
        name_upper = self.name.upper() if isinstance(self.name, str) else self.name
        # partner_name_upper = self.partner_id.parent_id if self.partner_id.parent_id else '' 
        partner_name_upper = self.partner_id.parent_id.name.upper() if self.partner_id.parent_id else '' 
        partner_calle = self.partner_id.street_name.upper() if self.partner_id.street_name else ''
        partner_numero = self.partner_id.street_number.upper() if self.partner_id.street_number else ''
        partner_colonia = self.partner_id.l10n_mx_edi_colony.upper() if self.partner_id.l10n_mx_edi_colony else ''
        partner_ciudad = self.partner_id.city.upper() if self.partner_id.city else ''
        partner_estado = self.partner_id.state_id.name.upper() if self.partner_id.state_id.name else ''
        partner_cp = self.partner_id.zip.upper() if self.partner_id.zip else ''
        partner_pais = self.partner_id.country_id.name.upper() if self.partner_id.country_id.name else ''

        
        qr_text = f"FECHA: {fecha_2_upper}, FOLIO: {name_upper}, GENERADOR: {partner_name_upper}, {partner_calle} {partner_numero}, {partner_colonia}, {partner_ciudad}, {partner_estado}, {partner_cp}, {partner_pais}, PROVEEDOR: {emp_tralisol_display}"
        return qr_text


    pdf_content = fields.Binary(string='PDF Content')


    def generar_imprimir_firma(self):
        self.ensure_one()
            
        
        try:
            _logger.info('Iniciando generación de firma para el registro con ID: %s', self.id)
            
            # Obtener el informe por su referencia
            report_ref = self.env.ref('manifiestos.manifiestos_manifiesto_jal_2_report', raise_if_not_found=False)
            if not report_ref:
                _logger.error('El informe con referencia manifiestos.manifiestos_manifiesto_jal_2_report no existe.')
                raise UserError('El informe no existe.')
            
            _logger.info('Informe encontrado: %s', report_ref)

            # Generar el PDF utilizando el método _render_qweb_pdf
            export_pdf = self.env["ir.actions.report"].sudo()._render_qweb_pdf(
                report_ref, res_ids=[self.id])[0]
            
            pdf_content = base64.encodebytes(export_pdf)
            _logger.info('PDF codificado en base64: %s', pdf_content)
            
            if not pdf_content:
                _logger.error('Error al generar el PDF para el registro con ID: %s', self.id)
                raise UserError('Error al generar el PDF.')
            
            self.pdf_content = pdf_content
            _logger.info('PDF generado y codificado en base64 correctamente para el registro con ID: %s', self.id)
            
        except Exception as e:
            _logger.error('Error al generar el PDF: %s', str(e))
            raise UserError(f'Error al generar el PDF: {str(e)}')



        # Crear el adjunto
        attachment = self.env['ir.attachment'].create({
            'name': f'{self.name}.pdf',
            'datas': self.pdf_content,
            'res_model': 'sign.template',
            'res_id': 0,
        })

        # Crear la plantilla de firma
        template = self.env['sign.template'].create({
            'attachment_id': attachment.id,
            'name': f'Template for {self.name}',
        })

        self.write({'firma_id_2': template.id})


        # Aquí puedes agregar cualquier otra lógica que necesites después de generar el PDF
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sign.template',
            'view_mode': 'form',
            'res_id': template.id,
            'target': 'current',
        }


    # def generar_imprimir_firma(self):
    #     self.ensure_one()
        
    #     try:
    #         _logger.info('Iniciando generación de firma para el registro con ID: %s', self.id)
            
    #         # Verificar la existencia del informe
    #         report_ref = self.env.ref('manifiestos.manifiestos_manifiesto_jal_2_report', raise_if_not_found=False)
    #         if not report_ref:
    #             _logger.error('El informe manifiestos.manifiestos_manifiesto_jal_2_report no existe.')
    #             raise UserError('El informe manifiestos.manifiestos_manifiesto_jal_2_report no existe.')
            
    #         _logger.info('Informe encontrado: %s', report_ref)

    #         # Generar el PDF
    #         report = report_ref._render_qweb_pdf(self.id)
    #         pdf_content = base64.b64encode(report[0])
    #         if not pdf_content:
    #             _logger.error('Error al generar el PDF para el registro con ID: %s', self.id)
    #             raise UserError('Error al generar el PDF.')
    #         self.pdf_content = pdf_content

    #         _logger.info('PDF generado correctamente para el registro con ID: %s', self.id)

    #         # Crear el adjunto
    #         attachment = self.env['ir.attachment'].create({
    #             'name': f'{self.name}.pdf',
    #             'datas': self.pdf_content,
    #             'res_model': 'sign.template',
    #             'res_id': 0,
    #         })

    #         _logger.info('Adjunto creado con ID: %s', attachment.id)

    #         # Crear la plantilla de firma
    #         template = self.env['sign.template'].create({
    #             'attachment_id': attachment.id,
    #             'name': f'Template for {self.name}',
    #         })

    #         _logger.info('Plantilla de firma creada con ID: %s', template.id)

    #         self.write({'firma_id_2': template.id})

    #         # Aquí puedes agregar cualquier otra lógica que necesites después de generar el PDF
    #         return {
    #             'type': 'ir.actions.act_window',
    #             'res_model': 'sign.template',
    #             'view_mode': 'form',
    #             'res_id': template.id,
    #             'target': 'current',
    #         }
    #     except Exception as e:
    #         _logger.error('Error al generar la firma: %s', str(e))
    #         raise UserError(f'Error al generar la firma: {str(e)}')







    # def generar_pdf(self):
    #     # Aquí se genera el PDF
    #     report = self.env.ref('manifiestos.manifiestos_manifiesto_jal_2_report')._render_qweb_pdf(self.id)
    #     pdf_content = base64.b64encode(report[0])
    #     return pdf_content

    # def imprimir(self):
    #     self.ensure_one()
    #     pdf_content = self.generar_pdf()
    #     if not pdf_content:
    #         raise UserError('Error al generar el PDF.')
    #     self.pdf_content = pdf_content

    #     # Aquí puedes agregar cualquier otra lógica que necesites después de generar el PDF
    #     return {
    #         'type': 'ir.actions.client',
    #         'tag': 'reload',
    #     }

    # def iniciar_proceso_firma(self):
    #     self.ensure_one()
    #     # Verificar que pdf_content no esté vacío
    #     if not self.pdf_content:
    #         raise UserError('El contenido del PDF está vacío.')

    #     # Crear el adjunto
    #     attachment = self.env['ir.attachment'].create({
    #         'name': f'{self.name}.pdf',
    #         'datas': self.pdf_content,
    #         'res_model': 'sign.template',
    #         'res_id': 0,
    #     })

    #     # Crear la plantilla de firma
    #     template = self.env['sign.template'].create({
    #         'attachment_id': attachment.id,
    #         'name': f'Template for {self.name}',
    #     })

    #     self.write({'firma_id_2': template.id})

    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'sign.template',
    #         'view_mode': 'form',
    #         'res_id': template.id,
    #         'target': 'current',
    #     }

    def actualizar_firma_id_1(self):
        # Buscar el registro de sign.request utilizando el valor de firma_id_2
        sign_request_record = self.env['sign.request'].search([('template_id', '=', self.firma_id_2.id)], limit=1)
        _logger.info('ID registro: %s', self.firma_id_2.id)
        if not sign_request_record:
            raise UserError(f'No se encontró ningún registro de sign.request con la plantilla {self.firma_id_2.name}.')

        # Actualizar el campo firma_id_1 con el ID del registro encontrado
        self.write({'firma_id_1': sign_request_record.id})

    # def action_start_signature_process(self):
    #     # Generar el archivo PDF
    #     pdf_content = self.env.ref('manifiestos.manifiestos_manifiesto_jal_2_report')._render_qweb_pdf(self.id)[0]
    #     pdf_base64 = base64.b64encode(pdf_content)

    #     # Crear el registro en el módulo de firma electrónica
    #     sign_request = self.env['sign.request'].create({
    #         # 'template_id': self.env.ref('your_sign_template_id').id,
    #         'template_id': self.env.ref('__export__.sign_template_54_3fc5a177').id,
    #         'reference': 'Manifiesto %s' % self.name,
    #         'request_item_ids': [(0, 0, {
    #             # 'partner_id': self.contact_id.id,
    #             'partner_id': self.partner_id.id,
    #             'role_id': self.env.ref('sign.sign_item_role_customer').id,
    #         })],
    #         'attachment_ids': [(0, 0, {
    #             'name': 'Manifiesto.pdf',
    #             'datas': pdf_base64,
    #             'res_model': 'manifiestos.manifiesto',
    #             'res_id': self.id,
    #         })],
    #     })

    #     # Actualizar el campo firma_id_1 con el nuevo registro de firma
    #     self.firma_id_1 = sign_request.id

    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'sign.request',
    #         'view_mode': 'form',
    #         'res_id': sign_request.id,
    #         'target': 'current',
    #     }

    estado = fields.Selection([
        ('ags', 'Aguascalientes'),
        ('gto', 'Guanajuato'),
        ('jal', 'Jalisco'),
    ], string='Estado de Manifiesto', required=True)

    auto_bd_man = fields.Selection([
        ('bd', 'Tralisol'),
        ('man', 'Manual'),
    ], string='Transporte', required=True)

    auto_tipo = fields.Char(string='Tipo de vehiculo', required=False)
    auto_placa = fields.Char(string='No. de Placa', required=False)



    

    acopio = fields.Selection([
        ('sel', 'Selecciona'),
        ('aco', 'Acopio'),
        ('reg', 'Destino'),
        ('dob', 'Destino y Acopio'),
    ], string='Tipo Destino', required=True, default='sel')

    chofer_nombre = fields.Char(string='Nombre Chofer', required=False)
    chofer_licencia = fields.Char(string='Licencia Chofer', required=False)
    chofer_tipo = fields.Char(string='Tipo Chofer', required=False)
    chofer_cargo = fields.Char(string='Cargo Chofer', required=False)
 
 
    estado = fields.Selection([
        ('ags', 'Aguascalientes'),
        ('gto', 'Guanajuato'),
        ('jal', 'Jalisco'),
    ], string='Estado', required=True, tracking=True)


    consecutivo = fields.Char(string='Consecutivo', readonly=True, copy=False, tracking=True)
    num_mani = fields.Integer(string='Número de Manifiesto', readonly=True, copy=False)
    # num_mani = fields.Char(string='Numero de Generador', required=True)


 

    @api.depends('firma_id_1')
    def _compute_firma_state(self):
        for record in self:
            record.firma_state = record.firma_id_1.state if record.firma_id_1 else ''

    @api.depends('firma_id_1')
    def _compute_firma_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for record in self:
            if record.firma_id_1:
                # document_id = record.firma_id.id if record.firma_id else 0
                record.firma_url = f"{base_url}/sign/document/{record.firma_id_1.id}/{record.firma_id_1.access_token}"
                # record.firma_url = f"{base_url}/sign/document/{record.firma_id.id}"
            else:
                record.firma_url = ''

#Elimina Fondo
    def _remove_background(self, image_data):
        # Decodificar la imagen de base64
        input_image = base64.b64decode(image_data)
        
        # Eliminar el fondo
        output_image = remove(input_image)
        
        # Convertir la imagen resultante a base64
        return base64.b64encode(output_image)


    @api.depends('consecutivo')
    def _compute_name(self):
        for record in self:
            record.name = record.consecutivo

    @api.model
    def create(self, vals):
        # Calcula el consecutivo solo al crear un nuevo registro
        if 'estado' in vals:
            vals['consecutivo'], vals['num_mani'] = self._generate_consecutivo(vals['estado'])
        # Procesar la imagen de la firma del chofer si está presente
        
        # 25
        # if 'f_firma_chofer' in vals:
        #     vals['f_firma_chofer'] = self._remove_background(vals['f_firma_chofer']) 
        return super(Manifiesto, self).create(vals)
        

    def write(self, vals):
        # Actualiza el consecutivo solo si el estado cambia
        if 'estado' in vals:
            for record in self:
                vals['consecutivo'], vals['num_mani'] = self._generate_consecutivo(vals['estado'])
        # 25        
        # if 'f_firma_chofer' in vals:
        #     vals['f_firma_chofer'] = self._remove_background(vals['f_firma_chofer'])  
        return super(Manifiesto, self).write(vals)

    def _generate_consecutivo(self, estado):
        # Puedes definir una lógica personalizada para generar el consecutivo
        if estado == 'ags':
            prefix = 'AGS'
        elif estado == 'gto':
            prefix = 'GTO'
        elif estado == 'jal':
            prefix = 'JAL'

        # Consulta la base de datos para contar registros existentes con el mismo estado
        count_consecutivo = self.search_count([('estado', '=', estado)])

        # Formatea el consecutivo con un prefijo y ceros a la izquierda
        new_consecutivo = f'{prefix}-{count_consecutivo + 1:06d}'
        return new_consecutivo, count_consecutivo + 1

    

    @api.depends('estado')
    def _compute_permiso(self):
        for record in self:
            if record.estado:
                # Puedes definir una lógica personalizada para generar el consecutivo
                if record.estado == 'ags':
                    prefix = 'SSMAA-GIR-RT-665-22'
                elif record.estado == 'gto':
                    prefix = 'IRA-PRME-059/2009'
                elif record.estado == 'jal':
                    prefix = 'DR 0817/18'

                record.emp_permiso = prefix




    def imprimir_manifiesto(self):
        self.ensure_one()
        # Obtener el reporte
        report = self.env.ref('manifiestos.report_manifiesto_jal_2_report')
        if report:
            # Generar el PDF
            pdf_data, _ = report.render_qweb_pdf(self.id)
            self.pdf_file = base64.b64encode(pdf_data).decode('utf-8')  # Almacenar el PDF en el campo pdf_file
            return {
                'type': 'ir.actions.report',
                'report_name': 'manifiestos.report_manifiesto_jal_2',
                'datas': {
                    'model': 'manifiestos.manifiesto',
                    'id': self.id,
                    'report_type': 'qweb-pdf'
                },
                'report_type': 'qweb-pdf',
                'data': {'model': 'manifiestos.manifiesto', 'id': self.id},
                'name': 'Manifiesto Report'
            }
        else:
            raise ValueError("No se encontró el informe 'manifiestos.report_manifiesto_jal_2_report'.")




class ManifiestoLine(models.Model):
    _name = 'manifiestos.line'
    _description = 'Línea de facturación del manifiesto'

    manifiesto_id = fields.Many2one('manifiestos.manifiesto', string='Manifiesto')
    product_id = fields.Many2one('product.product', string='Producto')
    tipo = fields.Char(string='Tipo')
    cantidad = fields.Float(string='Cantidad')
    capacidad = fields.Float(string='Capacidad')
    unidad = fields.Char(string='Unidad')
    clasifi_gto = fields.Selection([
        ('opc1', 'No aplica'),
        ('opc2', 'RR'),
        ('opc3', 'RNV'),
    ], string='CLASIFICACIÓN', default='opc1')


class ManifiestoReport(models.AbstractModel):

    _name='report.manifiestos.report_manifiesto_card'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('manifiestos.report_manifiesto_card')
        docs = self.env['manifiestos.manifiesto'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': self.env['manifiestos.manifiesto'],
            # 'docs': self.env['manifiestos.manifiesto'].browse(docids),
            'docs': docs,
            'employee_signature': docs.vehicle_id.conductor.f_rcontrol if docs.vehicle_id and docs.vehicle_id.conductor else None,
        }


#Firma automatica

    # def action_download_pdf(self):
    #     self.ensure_one()
    #     # Comprobar si el archivo PDF existe
    #     if not self.pdf_file:
    #         raise UserError("El archivo PDF no está disponible.")
    #     # Crear la URL de descarga
    #     pdf_filename = f"{self.name}.pdf"
    #     return {
    #         'type': 'ir.actions.act_url',
    #         'url': f'/web/content/?model={self._name}&id={self.id}&field=pdf_file&download=true&filename={pdf_filename}',
    #         'target': 'self',
    #     }


    # def action_create_signature_request(self):
    #     self.ensure_one()
    #     if not self.pdf_file:
    #         raise UserError("El archivo PDF no está disponible.")

    #     firma_request = self.env['sign.request'].create({
    #         'reference': self.name,
    #         'pdf_file': self.pdf_file,
    #         'signers': [(0, 0, {
    #             'partner_id': self.signer_partner_id.id,
    #             'signer_sequence': 1,
    #         })]
    #     })

    #     return {
    #         'name': 'Firma Electrónica',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'sign.request',
    #         'view_mode': 'form',
    #         'res_id': firma_request.id,
    #         'target': 'new',
    #     }


# class SignDocumentWizard(models.TransientModel):
#     _name = 'sign.document.wizard'
#     _description = 'Sign Document Wizard'

#     name = fields.Char(string='Document Name', required=True)
#     file = fields.Binary(string='File', required=True)
#     file_name = fields.Char(string='File Name', required=True)

#     def action_confirm(self):
#         self.ensure_one()
#         # Crear un nuevo registro en el modelo de firma electrónica
#         self.env['sign.document'].create({
#             'name': self.name,
#             'attachment_id': self.env['ir.attachment'].create({
#                 'name': self.file_name,
#                 'datas': self.file,
#                 'res_model': 'sign.document',
#             }).id,
#         })
#         return {'type': 'ir.actions.act_window_close'}

    # @api.depends('firma_id')
    # def _compute_firma_url(self):
    #     base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #     for record in self:
    #         if record.firma_id:
    #             # document_id = record.firma_id.id if record.firma_id else 0
    #             record.firma_url = f"{base_url}/sign/document/{record.firma_id.id}/{record.firma_id.access_token}"
    #             # record.firma_url = f"{base_url}/sign/document/{record.firma_id.id}"
    #         else:
    #             record.firma_url = ''


    # firma_id_1= fields.Many2one('sign.request', string='Firma Documento')
    # firma_id = fields.Many2one('sign.request.item', string='Firma Documento')
    # firma_id = fields.Char(string='Firma Item', compute='_compute_firma_item')
    # firma_state = fields.Char(string='Estado de la Firma', compute='_compute_firma_state')

    # @api.depends('firma_id_1')
    # def _compute_firma_item(self):
    #     for record in self:
    #         record.firma_id = record.firma_id.item if record.firma_id_1 else ''

        #consecutivo = fields.Char(string='Consecutivo', compute='_compute_consecutivo', store=True)

    #Los permisos ahora estan en el modulo de contacto
    #emp_permiso = fields.Selection([
    #    ('opc1', 'IMADES 393/2022'),
    #    ('opc2', 'DR 0817/18'),
    #    ('opc3', 'IRA-PRME-059/2009'),
    #    ('opc4', 'SSMAA-GIR-RT-665-22'),
    #    ('opc5', 'ERRME-12-22'),
    #    ('opc6', 'DR 0759/18'),
    #], string='Permiso Gobierno', required=True)



    #Los permisos ahora estan en el modulo de contacto
    # num_autorizacion = fields.Selection([
    #     ('opc1', 'DREMI1405300046/CA/CO/RE/18'),
    #     ('opc2', 'DEMI1409800691/CA/17'),
    #     ('opc3', 'DEMI1405301078/CO/'),
    #     ('opc4', 'IMADES DGA.PS. 009/2023'),
    # ], string='Numero autorización', required=True)

    # des_nombre = fields.Selection([
    #     ('opc1', 'EDUARDO ERNESTO SERRANO SERRANO/ P.A. OLIVIA EUNICE OSORNIO MACIAS'),
    #     ('opc2', 'GUILLERMO CHAIM SERRANO'),
    #     ('opc3', 'MARICELA CONTRERAS'),
    # ], string='Nombre Representante')

    # cargo = fields.Selection([
    #     ('opc1', 'REPRESENTANTE TÉCNICO'),
    #     ('opc2', 'REPRESENTANTE LEGAL'),
    #     ('opc3', 'COORDINADORA DE OPERACIONES'),
    # ], string='Cargo')



    #El QR lleva mayusculas
    # def generate_qr_code_text(self):
    #     emp_tralisol_display = dict(self._fields['emp_tralisol'].selection).get(self.emp_tralisol, 'Valor Desconocido')
    #     qr_text = f"FECHA: {self.fecha_2}, FOLIO: {self.name}, GENERADOR: {self.partner_id.name}, PROVEEDOR: {emp_tralisol_display}"
    #     return qr_text
    