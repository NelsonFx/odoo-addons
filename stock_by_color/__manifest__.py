{
    'name': 'Stock by Color',
    'version': '1.1',
    'category': 'Inventory',
    'summary': 'Inventario por color, tipo y marca (vista pivot de filamentos)',
    'depends': ['stock', 'product'],
    'data': [
        'views/stock_quant_views.xml',
    ],
    'installable': True,
    'application': False,
}
