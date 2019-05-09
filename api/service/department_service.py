from sqlalchemy_utils import sort_query

from api.model.course import Course
from api.model.department import Department
from api.utils.helpers import sort_and_paginate


def get_all_departments(page, page_size, order_by, term_id=None):
    query = Department.query
    if term_id is not None:
        ids_subquery = Course.query.with_entities(Course.department_id).filter_by(term_id=term_id).distinct()
        query = query.filter(Department.id.in_(ids_subquery))
    sql_results = sort_and_paginate(query, order_by, page, page_size).all()
    return [dep.as_dict() for dep in sql_results]


def search_departments(query, page, page_size):
    return [obj.as_dict() for obj in Department.search(query, page, page_size)]


def search_highlights_departments(query, page, page_size):
    return Department.highlights(query, page, page_size)


def get_single_department(department_id):
    result = Department.query.get(department_id)
    return result.as_dict() if result is not None else result
