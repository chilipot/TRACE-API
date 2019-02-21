from flask import session
from sqlalchemy.orm import contains_eager
from sqlalchemy_utils import sort_query

from app.main.model.tables import Term, Instructor, Report


def get_all_terms(page, page_size, sort):
    return sort_query(Term.query, sort).paginate(page, page_size, False).items


def get_term(term_id):
    return Term.query.get(term_id)


def get_all_instructors(page, page_size, sort):
    sql_results = sort_query(Instructor.query, sort).paginate(page, page_size, False).items
    return [Instructor.as_dict(inst) for inst in sql_results]


def get_instructor(instructor_id):
    return Instructor.query.get(instructor_id)


def get_all_course_reports(page, page_size, sort):
    sql_results = sort_query(Report.query.join(Report.Term).join(Report.Instructor).options(
        contains_eager(Report.Term)).options(contains_eager(Report.Instructor)), sort).paginate(page, page_size,
                                                                                                False).items
    return [Report.as_dict(obj) for obj in sql_results]


def search_course_reports(query, page, page_size):
    if session.get('cached_terms', None) is None:
        session['cached_terms'] = [x.Title.split(":")[-1].strip().replace(' - ', ' ')
                                   for x in Term.query.with_entities(Term.Title).all()]
    return [Report.as_dict(obj) for obj in Report.search(query, page, page_size)]


def get_course_report(report_id):
    return Report.query.get(report_id)
