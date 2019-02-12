# coding: utf-8
import datetime

import jwt
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, NCHAR, Unicode
from sqlalchemy.dialects.mssql import BIT
from sqlalchemy.orm import relationship
from .. import db, flask_bcrypt
from ..config import key


class BlacklistToken(db.Model):
    __tablename__ = 'BlacklistToken'

    ID = Column(Integer, primary_key=True, unique=True)
    Token = Column(NCHAR(500), nullable=False)
    BlacklistedOn = Column(DateTime, nullable=False)

    def __init__(self, token):
        self.Token = token
        self.BlacklistedOn = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.Token)

    @staticmethod
    def check_blacklist(auth_token):
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False


class Instructor(db.Model):
    __tablename__ = 'Instructor'

    InstructorID = Column(Integer, primary_key=True)
    FirstName = Column(Unicode(100), nullable=False)
    LastName = Column(Unicode(100), nullable=False)
    MiddleName = Column(Unicode(100))


class LookupAnswerText(db.Model):
    __tablename__ = 'Lookup_AnswerText'

    AnswerTextID = Column(Integer, primary_key=True)
    Text = Column(Unicode(500), nullable=False)


class LookupQuestionText(db.Model):
    __tablename__ = 'Lookup_QuestionText'

    QuestionTextID = Column(Integer, primary_key=True)
    Abbrev = Column(Unicode(250), nullable=False)
    Text = Column(Unicode(500), nullable=False)


class Term(db.Model):
    __tablename__ = 'Term'

    TermID = Column(Integer, primary_key=True)
    Title = Column(Unicode(200), nullable=False)


class User(db.Model):
    __tablename__ = 'User'

    ID = Column(Integer, primary_key=True)
    Email = Column(Unicode(255), nullable=False, unique=True)
    RegisteredOn = Column(DateTime, nullable=False)
    Admin = Column(BIT, nullable=False)
    PublicID = Column(Unicode(100), unique=True)
    Username = Column(Unicode(50), unique=True)
    PasswordHash = Column(Unicode(100))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.PasswordHash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.PasswordHash.encode(), password)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS512'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key, algorithms=['HS512'])
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<User '{}'>".format(self.Username)


class Report(db.Model):
    __tablename__ = 'Report'

    ReportID = Column(Integer, primary_key=True)
    CourseID = Column(Integer, nullable=False)
    InstructorID = Column(ForeignKey('Instructor.InstructorID'), nullable=False)
    TermID = Column(ForeignKey('Term.TermID'), nullable=False)
    Name = Column(Unicode(500), nullable=False)
    Subject = Column(Unicode(50), nullable=False)
    Number = Column(Integer, nullable=False)
    Section = Column(Unicode(20))

    Instructor = relationship('Instructor')
    Term = relationship('Term')


class ScoreDatum(db.Model):
    __tablename__ = 'ScoreData'

    DataID = Column(Integer, primary_key=True)
    ReportID = Column(ForeignKey('Report.ReportID'), nullable=False)
    Enrollment = Column(Integer, nullable=False)
    Responses = Column(Integer, nullable=False)
    Declines = Column(Integer, nullable=False)

    Report = relationship('Report')


class Question(db.Model):
    __tablename__ = 'Question'

    QuestionID = Column(Integer, primary_key=True)
    DataID = Column(ForeignKey('ScoreData.DataID'), nullable=False)
    QuestionTextID = Column(ForeignKey('Lookup_QuestionText.QuestionTextID'), nullable=False)
    ResponseCount = Column(Integer, nullable=False)
    ResponseRate = Column(Float(53), nullable=False)
    Mean = Column(Float(53), nullable=False)
    Median = Column(Float(53), nullable=False)
    StdDev = Column(Float(53), nullable=False)

    ScoreDatum = relationship('ScoreDatum')
    Lookup_QuestionText = relationship('LookupQuestionText')


class Answer(db.Model):
    __tablename__ = 'Answer'

    AnswerID = Column(Integer, primary_key=True)
    AnswerTextID = Column(ForeignKey('Lookup_AnswerText.AnswerTextID'), nullable=False)
    QuestionID = Column(ForeignKey('Question.QuestionID'), nullable=False)
    Value = Column(Integer, nullable=False)

    Lookup_AnswerText = relationship('LookupAnswerText')
    Question = relationship('Question')
