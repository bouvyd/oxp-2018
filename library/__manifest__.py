{
    'name': 'Library',
    'summary': 'Manage a library',
    'depends': ['mail'],
    'version': '1.0',
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/library_views.xml',
    ],
    'demo': [
        'data/demo.xml'
    ],
}
