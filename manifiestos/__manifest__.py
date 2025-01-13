{
    'name': 'Manifiestos',
    'version': '17.0.0.1',
    'summary': 'Aplicación para registrar manifiestos de residuos.',
    'author': 'Fernando Rodriguez',
    'depends': ['base','web','product','hr','sign'],  # Dependencias de otros módulos
    'data': [
        'reports/manifiesto_reports.xml',
        'views/manifiesto_view.xml',
        'views/templates.xml',
        'reports/manifiesto_solojal_2.xml',
        'reports/manifiesto_factura.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
