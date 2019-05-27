from api.model import Course, ScoreData, Term, Instructor, Department


def get_all_courses(page, page_size, order_by, facets={}):
    from api.utils.helpers import sort_and_paginate, apply_sql_facets
    query = Course.query
    if facets:
        query = apply_sql_facets(Course, query, facets)

    query = query.join(Term).join(Instructor).join(Department)

    sql_results = sort_and_paginate(query, order_by, page, page_size).all()
    return sql_results


def search_courses(query, page, page_size, facets={}):
    return (obj.as_dict() for obj in Course.search(query, page, page_size, facets=facets))


def search_highlights_courses(query, page, page_size, facets={}):
    return Course.highlights(query, page, page_size, facets=facets)


def get_single_course(report_id):
    result = Course.query.get(report_id).join(Term).join(Instructor).join(Department)
    return result.as_dict() if result is not None else result


def get_single_report(report_id):
    report = ScoreData.query.filter_by(report_id=report_id).first()
    return report.as_dict()
