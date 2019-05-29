from api.instructor.service import get_all_instructors, get_single_instructor, search_instructors, \
    search_highlights_instructors
from api.utils.constants import DEFAULT_PAGE_SIZE
from api.utils.helpers import Serverless


@Serverless.route
def get_instructors():
    """
    List all instructors
    """
    page = Serverless.args.get('page', 1, int)
    page_size = Serverless.args.get('pageSize', DEFAULT_PAGE_SIZE, int)
    order_by = Serverless.args.get('orderBy', 'id', str)
    term_id = Serverless.args.get('term_id', None, str)
    department_id = Serverless.args.get('department_id', None, str)
    query = Serverless.args.get('query', '', str)
    highlights = Serverless.args.get('highlights', False, bool)

    params = dict(query=query, page=page, page_size=page_size, order_by=order_by, term_id=term_id,
                  department_id=department_id)

    operation = get_all_instructors
    if query:
        operation = search_instructors if not highlights else search_highlights_instructors
        params = {k: v for k, v in params.items() if k not in ['order_by', 'term_id', 'department_id']}
    else:
        params.pop('query')

    results = operation(**params)

    return results, 200


@Serverless.route
def get_instructor(instructor_id):
    """
    Get an instructor given its identifier
    """
    instructor = get_single_instructor(instructor_id)
    if not instructor:
        Serverless.abort(404)
    else:
        return instructor, 200
