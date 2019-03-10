import datetime
import uuid

from src.model.tables import User
from src.model import db


def save_new_user(data):
    user = User.query.filter_by(Email=data['email']).first()
    if data['username'] is None or data['password'] is None:
        response_object = {
            'status': 'failure',
            'message': 'Missing arguments.',
        }
        return response_object, 400
    if not user:
        new_user = User(
            PublicID=str(uuid.uuid4()),
            Email=data['email'],
            Admin=data['admin'],
            Username=data['username'],
            password=data['password'],
            RegisteredOn=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        response_object = {
            'status': 'success',
            'message': 'User created. Please Log in.',
        }

        return response_object, 200
    else:
        response_object = {
            'status': 'failure',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return [u.as_dict() for u in User.query.all()]


def get_a_user(public_id):
    return User.query.filter_by(PublicID=public_id).first().as_dict()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
