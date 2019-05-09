from sqlalchemy_utils import sort_query

from api.model.instructor import Instructor


def get_all_instructors(page, page_size, sort):
    sql_results = sort_query(Instructor.query, sort).paginate(page, page_size, False).items
    return [inst.as_dict() for inst in sql_results]


def get_single_instructor(instructor_id):
    result = Instructor.query.get(instructor_id)
    return result.as_dict() if result is not None else result
