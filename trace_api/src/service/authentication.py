from flask_httpauth import HTTPTokenAuth
import os
from redis import Redis
import secrets
from flask import g
from src import redis_pool

rds = Redis(connection_pool=redis_pool)
SECRET_KEY = os.getenv('SECRET_KEY')


def refresh_token(self):
    self.Token = secrets.token_urlsafe(20)


def generate_token(user):
    token = secrets.token_urlsafe(20)
    print('*** token for {}: {}\n'.format(user, token))
    if rds.set(token, user):
        return token
    else:
        print('error')
        return None


def configure_auth(flask_auth: HTTPTokenAuth) -> HTTPTokenAuth:
    @flask_auth.verify_token
    def verify_token(token):
        g.user = None
        try:
            data = rds.get(token)
        except:
            return False
        if data:
            g.user = data
            return True
        return False

    @flask_auth.error_handler
    def handle_error():
        return "Authentication Error Occurred"

    print('Authentication setup')

    return flask_auth


auth_inst = HTTPTokenAuth(scheme='Bearer')
auth = configure_auth(auth_inst)
