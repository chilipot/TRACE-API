from flask_restplus import Resource
from flask import request, jsonify
from src.util.dto import AuthDto
from src.model.tables import User
from src.service.authentication import auth, generate_token

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.errorhandler(Exception)
def auth_error_handler(error):
    """
    Namespace error handler
    """
    return {'message': f"#AUTH {str(error)}"}, getattr(error, 'code', 500)


@api.route('/login')
class UserLogin(Resource):
    """
    User Login Resource
    """

    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        print('logging in')
        data = request.json
        # get the post data
        user = User.query.filter_by(Email=data.get('email')).first()
        if user and user.check_password(data.get('password')):
            print(user.Username)
            token = generate_token(user.Username)
        else:
            res = jsonify({"message": "Bad username or password"})
            res.status_code = 401
            return res

        ret = {
            "token": token
        }
        res = jsonify(ret)
        res.status_code = 200
        return res


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """

    @auth.login_required
    @api.doc('logout a user')
    def post(self):
        pass
