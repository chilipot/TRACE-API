import flask
from sqlalchemy.orm import load_only

from api import db_session
from api.model import Course, ScoreData, Term, Instructor, Comment, Department, Response
from api.utils.helpers import sort_and_paginate, apply_sql_facets, get_or_abort


def get_all_courses(page, page_size, order_by, facets={}):
    query = Course.query
    if facets:
        query = apply_sql_facets(Course, query, facets)

    query = query.join(Term).join(Instructor).join(Department)

    sql_results = sort_and_paginate(query, order_by, page, page_size).all()
    return [obj.as_dict() for obj in sql_results]


def search_courses(query, page, page_size, facets={}):
    return [obj.as_dict() for obj in Course.search(query, page, page_size, facets=facets)]


def search_highlights_courses(query, page, page_size, facets={}):
    return Course.highlights(query, page, page_size, facets=facets)


def get_single_course(report_id):
    result = Course.query.get(report_id)
    return result.as_dict() if result is not None else result


def get_single_report(report_id):
    report = ScoreData.query.filter_by(report_id=report_id).join(Course).first()
    if report:
        result = report.as_dict()
        # TODO: Clean up logic
        result['comments'] = [c.text for c in
                              Comment.query.filter_by(report_id=report_id).with_entities(Comment.text).all()]
        result['id'] = report_id
        return result
    else:
        return None


def save_user_report_response(report_id, user_id, response_data):
    get_or_abort(Course, report_id)

    response_entries = []
    for q_id, ans_id in response_data.items():
        response_entries.append(Response(user_id, report_id, q_id, ans_id))
    try:
        if response_entries:
            db_session.add_all(response_entries)
            db_session.commit()
    except Exception:
        db_session.rollback()
        raise
