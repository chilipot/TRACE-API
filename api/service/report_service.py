from api.model import Course, ScoreData, Term, Instructor, Comment, Department
from api.utils.helpers import sort_and_paginate, apply_sql_facets


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
