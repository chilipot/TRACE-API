from sqlalchemy_utils import sort_query

from api.model.course import Course
from api.model.department import Department


def get_all_departments(page, page_size, sort, term_id=None):
    query = Department.query
    if term_id is not None:
        ids_subquery = Course.query.with_entities(Course.department_id).filter_by(term_id=term_id).distinct()
        query = query.filter(Department.id.in_(ids_subquery))
    sql_results = sort_query(query, sort).paginate(page, page_size, False).items
    return [dep.as_dict() for dep in sql_results]


def get_single_department(department_id):
    result = Department.query.get(department_id)
    return result.as_dict() if result is not None else result
