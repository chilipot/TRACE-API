# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, NCHAR, Unicode
from sqlalchemy.dialects.mssql import BIT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BlacklistToken(Base):
    __tablename__ = 'BlacklistToken'

    ID = Column(Integer, primary_key=True, unique=True)
    Token = Column(NCHAR(500), nullable=False)
    BlacklistedOn = Column(DateTime, nullable=False)


class Instructor(Base):
    __tablename__ = 'Instructor'

    InstructorID = Column(Integer, primary_key=True)
    FirstName = Column(Unicode(100), nullable=False)
    LastName = Column(Unicode(100), nullable=False)
    MiddleName = Column(Unicode(100))


class LookupAnswerText(Base):
    __tablename__ = 'Lookup_AnswerText'

    AnswerTextID = Column(Integer, primary_key=True)
    Text = Column(Unicode(500), nullable=False)


class LookupQuestionText(Base):
    __tablename__ = 'Lookup_QuestionText'

    QuestionTextID = Column(Integer, primary_key=True)
    Abbrev = Column(Unicode(250), nullable=False)
    Text = Column(Unicode(500), nullable=False)


class Term(Base):
    __tablename__ = 'Term'

    TermID = Column(Integer, primary_key=True)
    Title = Column(Unicode(200), nullable=False)


class User(Base):
    __tablename__ = 'User'

    ID = Column(Integer, primary_key=True)
    Email = Column(Unicode(255), nullable=False, unique=True)
    RegisteredOn = Column(DateTime, nullable=False)
    Admin = Column(BIT, nullable=False)
    PublicID = Column(Unicode(100), unique=True)
    Username = Column(Unicode(50), unique=True)
    PasswordHash = Column(Unicode(100))


class Report(Base):
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


class ScoreDatum(Base):
    __tablename__ = 'ScoreData'

    DataID = Column(Integer, primary_key=True)
    ReportID = Column(ForeignKey('Report.ReportID'), nullable=False)
    Enrollment = Column(Integer, nullable=False)
    Responses = Column(Integer, nullable=False)
    Declines = Column(Integer, nullable=False)

    Report = relationship('Report')


class Question(Base):
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


class Answer(Base):
    __tablename__ = 'Answer'

    AnswerID = Column(Integer, primary_key=True)
    AnswerTextID = Column(ForeignKey('Lookup_AnswerText.AnswerTextID'), nullable=False)
    QuestionID = Column(ForeignKey('Question.QuestionID'), nullable=False)
    Value = Column(Integer, nullable=False)

    Lookup_AnswerText = relationship('LookupAnswerText')
    Question = relationship('Question')
