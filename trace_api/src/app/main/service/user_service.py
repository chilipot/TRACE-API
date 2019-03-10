import datetime
import uuid

from app.main import db
from app.main.model.tables import User


def save_new_user(data):
    user = User.query.filter_by(Email=data['email']).first()
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
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.get(public_id)


def save_changes(data):
    db.session.add(data)
    db.session.commit()
