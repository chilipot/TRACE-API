from flask import request, session, jsonify
from flask_restplus import Resource

from ..util.dto import AuthDto
from flask_jwt_extended import jwt_required, get_raw_jwt, \
    jwt_refresh_token_required, get_jwt_identity
from ..model.tables import User
from .. import blacklist
from ..config import ACCESS_EXPIRES, REFRESH_EXPIRES
from flask_jwt_extended import create_access_token, create_refresh_token, \
    get_jti

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    """
    User Login Resource
    """

    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        data = request.json
        # get the post data
        user = User.query.filter_by(Email=data.get('email')).first()
        if user and user.check_password(data.get('password')):
            username = data.get('email', None)
        else:
            res = jsonify({"message": "Bad username or password"})
            res.status_code = 401
            return res

        # Create our JWTs
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        access_jti = get_jti(encoded_token=access_token)
        refresh_jti = get_jti(encoded_token=refresh_token)
        blacklist.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
        blacklist.set(refresh_jti, 'false', REFRESH_EXPIRES * 1.2)

        ret = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        res = jsonify(ret)
        res.status_code = 200
        return res


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """

    @jwt_required
    @api.doc('logout a user')
    def post(self):
        if session:
            session.clear()
        # get auth token
        jti = get_raw_jwt()['jti']
        blacklist.set(jti, 'true', ACCESS_EXPIRES * 1.2)
        res = jsonify({"msg": "Access token revoked"})
        res.status_code = 200
        return res


@api.route('/refresh')
class RefreshTokens(Resource):
    """
    Refresh access tokens
    """

    @jwt_refresh_token_required
    @api.doc('refresh access token')
    def post(self):
        current_user = get_jwt_identity()
        # Do the same thing that we did in the login endpoint here
        access_token = create_access_token(identity=current_user)
        access_jti = get_jti(encoded_token=access_token)
        blacklist.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
        res = jsonify({'access_token': access_token})
        res.status_code = 201
        return res
