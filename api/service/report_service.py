from api.model import Course, ScoreData, Term, Instructor
from api.utils.helpers import sort_and_paginate


def get_all_courses(page, page_size, order_by):
    query = Course.query.join(Term).join(Instructor)

    sql_results = sort_and_paginate(query, order_by, page, page_size).all()
    return [obj.as_dict() for obj in sql_results]


def search_courses(query, page, page_size):
    return [obj.as_dict() for obj in Course.search(query, page, page_size)]


def search_highlights_courses(query, page, page_size):
    return Course.highlights(query, page, page_size)


def get_single_course(report_id):
    result = Course.query.get(report_id)
    return result.as_dict() if result is not None else result


def get_single_report(report_id):
    report = ScoreData.query.filter_by(report_id=report_id).first()
    return report.as_dict()
