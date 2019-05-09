from sqlalchemy.orm import contains_eager
from sqlalchemy_utils import sort_query

from api.model.course import Course
from api.model.score_data import ScoreData
from api.utils.helpers import sort_and_paginate


def get_all_courses(page, page_size, order_by):
    query = Course.query.join(Course.term).join(Course.instructor).options(
        contains_eager(Course.term)).options(contains_eager(Course.instructor))

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
