from flask import session
from sqlalchemy_utils import sort_query

from app.main.model.tables import Term, Instructor, Report


def get_all_terms(page, page_size, sort):
    return sort_query(Term.query, sort).paginate(page, page_size, False).items


def get_term(term_id):
    return Term.query.filter_by(TermID=term_id).first()


def get_all_instructors(page, page_size, sort):
    return sort_query(Instructor.query, sort).paginate(page, page_size, False).items


def get_instructor(instructor_id):
    return Instructor.query.filter_by(InstructorID=instructor_id).first()


def get_all_course_reports(page, page_size, sort):
    if session['cached_terms'] is None:
        session['cached_terms'] = [x.Title.split(":")[-1].strip().replace(' - ', ' ')
                                   for x in Term.query.with_entities(Term.Title).all()]
    return sort_query(Report.query.join(Report.Term).join(Report.Instructor), sort).paginate(page, page_size,
                                                                                             False).items


def search_course_reports(query, page, page_size):
    if session.get('cached_terms', None) is None:
        session['cached_terms'] = [x.Title.split(":")[-1].strip().replace(' - ', ' ')
                                   for x in Term.query.with_entities(Term.Title).all()]
    return Report.search(query, page, page_size)


def get_course_report(report_id):
    return Report.query.filter_by(ReportID=report_id).first()
