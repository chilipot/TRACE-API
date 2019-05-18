from api.service.report_service import get_all_courses, get_single_course, get_single_report, \
    search_courses, search_highlights_courses
from api.utils.constants import DEFAULT_PAGE_SIZE
from api.utils.helpers import responsify, get_id_facets_from_request, Serverless


@Serverless.route
def get_courses():
    """
    List many courses
    """
    query = Serverless.args.get('query', '', str)
    page = Serverless.args.get('page', 1, int)
    page_size = Serverless.args.get('pageSize', DEFAULT_PAGE_SIZE, int)
    order_by = Serverless.args.get('orderBy', 'id', str)
    highlights = Serverless.args.get('highlights', False, bool)

    facets = get_id_facets_from_request(['department_id', 'instructor_id', 'term_id'])

    params = dict(query=query, page=page, page_size=page_size, order_by=order_by, facets=facets)

    operation = get_all_courses
    if query:
        operation = search_courses if not highlights else search_highlights_courses
        params.pop('order_by')
    else:
        params.pop('query')

    results = operation(**params)

    # jsonify made this slow :(
    return responsify(results, 200)


@Serverless.route
def get_course(report_id):
    """
    Get a course given its identifier
    """
    report = get_single_course(report_id)
    if not report:
        Serverless.abort(404)
    else:
        return responsify(report), 200


@Serverless.route
def get_scores(report_id):
    """
    Get a course report and scores given its identifier
    """
    report = get_single_report(report_id)
    if not report:
        Serverless.abort(404)
    else:
        # Avoiding jsonify because it can be slow
        return responsify(report, 200)
