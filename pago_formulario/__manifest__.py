{
    'name': 'Pagos Beeren',
    'version': '17.0.1.0',
    'license': 'LGPL-3',
    'author': 'Fernando Rodriguez C',
    'summary': 'Ajuste del formato de pago',
    'category': 'Accounting',
    'depends': [
        'account','product','producto_market'
    ],
    'data': [
        'views/pago_beeren.xml',
        'report/pagobeeren.xml',
    ],
    'installable': True,
    'auto_install': False,
}
