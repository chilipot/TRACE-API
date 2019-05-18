from api.model.course import Course
from api.model.instructor import Instructor
from api.utils.helpers import sort_and_paginate


def get_all_instructors(page, page_size, order_by, term_id=None, department_id=None):
    query = Instructor.query
    if term_id is not None or department_id is not None:
        filter_params = {**(term_id is not None and {'term_id': term_id} or {}),
                         **(department_id is not None and {'department_id': department_id} or {})}
        ids_subquery = Course.query.with_entities(Course.instructor_id).filter_by(**filter_params).distinct()
        query = query.filter(Instructor.id.in_(ids_subquery))
    sql_results = sort_and_paginate(query, order_by, page, page_size).all()
    return [inst.as_dict() for inst in sql_results]


def search_instructors(query, page, page_size):
    return [obj.as_dict() for obj in Instructor.search(query, page, page_size)]


def search_highlights_instructors(query, page, page_size):
    return Instructor.highlights(query, page, page_size)


def get_single_instructor(instructor_id):
    result = Instructor.query.get(instructor_id)
    return result.as_dict() if result is not None else result
