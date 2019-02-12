# from .. import db, flask_bcrypt
# import datetime
# import jwt
# from app.main.model.blacklist import BlacklistToken
# from ..config import key
#
# class User(db.Model):
#     """
#     User Model for storing user related details
#     """
#     __tablename__ = "user"
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     email = db.Column(db.String(255), unique=True, nullable=False)
#     registered_on = db.Column(db.DateTime, nullable=False)
#     admin = db.Column(db.Boolean, nullable=False, default=False)
#     public_id = db.Column(db.String(100), unique=True)
#     username = db.Column(db.String(50), unique=True)
#     password_hash = db.Column(db.String(100))
#
#
