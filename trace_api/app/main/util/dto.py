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
        'password': fields.String(required=True, description='The user password')
    })


class ReportDto:
    api = Namespace('course info', description='report related operations')
    term = api.model('term', {
        'TermID': fields.Integer(attribute='TermID', required=True, description='term id'),
        'Title': fields.String(attribute='Title', required=True, description='term name/title')
    })

    instructor = api.model('instructor', {
        'InstructorID': fields.Integer(attribute='InstructorID', required=True, description='instructor id'),
        'FirstName': fields.String(attribute='FirstName', required=True, description='instructor first name'),
        'MiddleName': fields.String(attribute='MiddleName', required=True, description='instructor middle name'),
        'LastName': fields.String(attribute='LastName', required=True, description='instructor last name')
    })

    course = api.model('course', {
        'ReportID': fields.Integer(attribute='ReportID', required=True, description='report id'),
        'CourseID': fields.Integer(attribute='CourseID', required=True, description='course id'),
        'Instructor': fields.Nested(instructor),
        'Term': fields.Nested(term),
        'Name': fields.String(attribute='Name', required=True, description='course name'),
        'Subject': fields.String(attribute='Subject', required=True, description='department code/subject of course'),
        'Number': fields.String(attribute='Number', required=True, description='course number'),
        'Section': fields.String(attribute='Section', description='section code/number for course')
    })
