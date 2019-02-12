from flask_restplus import Namespace, fields

"""
Data Transfer Objects are responsible for carrying data between processes 
"""


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(attribute='Email', required=True, description='user email address'),
        'username': fields.String(attribute='Username', required=True, description='user username'),
        'admin': fields.Boolean(attribute='Admin', required=True, default=False, description='user is admin?'),
        'password': fields.String(attribute='PasswordHash', required=True, description='user password'),
        'public_id': fields.String(attribute='PublicID', description='user Identifier')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(attribute='Email', required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password'),
    })
