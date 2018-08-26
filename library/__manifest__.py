{
    'name': 'Library',
    'summary': 'Manage a library',
    'depends': ['mail'],
    'version': '1.1',
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/library_views.xml',
    ],
    'demo': [
        'data/library_demo.xml'
    ],
}
