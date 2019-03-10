from flask import request
from flask_restplus import Resource

from src.service.user_service import save_new_user, get_all_users, get_a_user
from src.util.dto import UserDto
from src.service.authentication import auth


api = UserDto.api
_user = UserDto.user


@api.errorhandler
def user_error_handler(error):
    """
    Namespace error handler
    """
    return {'message': f"#USER {str(error)}"}, getattr(error, 'code', 500)


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    def get(self):
        """
        List all registered users
        """
        return get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """
        Creates a new User
        """
        data = request.json
        return save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @auth.login_required
    @api.doc('get a user')
    def get(self, public_id):
        """
        get a user given its identifier
        """
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user
