{
    'name': 'Final Assign',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Manage customer check-in/check-out and link to sale orders',
    'author': 'Your Name',
    'depends': ['sale','base','web'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/check_in_out_form_view.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'final_assign/static/src/js/*.js',
        ],
    },
    'installable': True,
    'application': True,
}
