# coding: utf-8

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, Unicode
from sqlalchemy.dialects.mssql import BIT
from sqlalchemy.orm import relationship

from app.main.model.mixins.mixins import SearchableMixin
from .. import db, flask_bcrypt


class Instructor(db.Model):
    __tablename__ = 'Instructor'

    InstructorID = Column(Integer, primary_key=True)
    FirstName = Column(Unicode(100), nullable=False)
    LastName = Column(Unicode(100), nullable=False)
    MiddleName = Column(Unicode(100))

    @property
    def full_name(self):
        return ' '.join(filter(lambda x: x is not None and x.strip(),
                               [self.FirstName, self.LastName]))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


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

    @property
    def normal_title(self):
        return self.Title.split(":")[-1].strip().replace(' - ', ' ')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


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
        self.PasswordHash = flask_bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.PasswordHash.encode(),
                                                password)

    def __repr__(self):
        return "<User '{}'>".format(self.Username)


class Report(SearchableMixin, db.Model):
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
    ScoreDatum = relationship('ScoreDatum', back_populates='Report',
                              uselist=False)

    @property
    def course_full_name(self):
        return f'{self.Subject}{self.Number} {self.Name}'

    def as_dict(self):
        fks = [fk.column.name for fk in self.__table__.foreign_keys]
        columns = {c.name: getattr(self, c.name) for c in self.__table__.columns
                   if c.name not in fks}
        columns['Instructor'] = self.Instructor.as_dict()
        columns['Term'] = self.Term.as_dict()
        return columns

    def as_report_dict(self):
        columns = {'Metadata': {
            'Course': self.course_full_name,
            'Term': self.Term.normal_title,
            'Instructor': self.Instructor.full_name
        }}
        columns.update(self.ScoreDatum.as_dict(no_primary_key=True))
        return columns


class ScoreDatum(db.Model):
    __tablename__ = 'ScoreData'

    DataID = Column(Integer, primary_key=True)
    ReportID = Column(ForeignKey('Report.ReportID'), nullable=False)
    Enrollment = Column(Integer, nullable=False)
    Responses = Column(Integer, nullable=False)
    Declines = Column(Integer, nullable=False)

    Report = relationship('Report', back_populates='ScoreDatum', uselist=False)
    Questions = relationship('Question', back_populates='ScoreDatum',
                             lazy='joined')

    def as_dict(self, no_primary_key=False):
        fks = [fk.column.name for fk in self.__table__.foreign_keys]
        pk = self.__table__.primary_key.columns.values()[0].name
        columns = {c.name: getattr(self, c.name) for c in self.__table__.columns
                   if
                   c.name not in fks and (no_primary_key and c.name != pk)}
        columns['Questions'] = [q.as_dict(no_primary_key=True) for q in
                                self.Questions]
        return columns


class Question(db.Model):
    __tablename__ = 'Question'

    QuestionID = Column(Integer, primary_key=True)
    DataID = Column(ForeignKey('ScoreData.DataID'), nullable=False)
    QuestionTextID = Column(ForeignKey('Lookup_QuestionText.QuestionTextID'),
                            nullable=False)
    ResponseCount = Column(Integer, nullable=False)
    ResponseRate = Column(Float(53), nullable=False)
    Mean = Column(Float(53), nullable=False)
    Median = Column(Float(53), nullable=False)
    StdDev = Column(Float(53), nullable=False)

    ScoreDatum = relationship('ScoreDatum', back_populates="Questions")
    LookupQuestionText = relationship('LookupQuestionText', lazy='joined')
    Answers = relationship('Answer', back_populates='Question', lazy='joined')

    def as_dict(self, no_primary_key=False):
        fks = [fk.column.name for fk in self.__table__.foreign_keys]
        pk = self.__table__.primary_key.columns.values()[0].name
        columns = {c.name: getattr(self, c.name) for c in self.__table__.columns
                   if
                   c.name not in fks and (no_primary_key and c.name != pk)}
        columns['Text'] = self.LookupQuestionText.Text
        columns['Answers'] = [a.as_dict(no_primary_key=True) for a in
                              self.Answers]
        return columns


class Answer(db.Model):
    __tablename__ = 'Answer'

    AnswerID = Column(Integer, primary_key=True)
    AnswerTextID = Column(ForeignKey('Lookup_AnswerText.AnswerTextID'),
                          nullable=False)
    QuestionID = Column(ForeignKey('Question.QuestionID'), nullable=False)
    Value = Column(Integer, nullable=False)

    LookupAnswerText = relationship('LookupAnswerText', lazy='joined')
    Question = relationship('Question', back_populates="Answers")

    def as_dict(self, no_primary_key=False):
        fks = [fk.column.name for fk in self.__table__.foreign_keys]
        pk = self.__table__.primary_key.columns.values()[0].name
        columns = {c.name: getattr(self, c.name) for c in self.__table__.columns
                   if
                   c.name not in fks and (no_primary_key and c.name != pk)}
        columns['Text'] = self.LookupAnswerText.Text
        return columns