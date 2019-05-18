import flask
from flask import request

from api.controller import api
from api.service.report_service import get_all_courses, get_single_course, get_single_report, \
    search_courses, search_highlights_courses
from api.utils.constants import DEFAULT_PAGE_SIZE
from api.utils.helpers import responsify, get_id_facets_from_request


@api.route('course')
def get_courses():
    """
    List many courses
    """
    query = request.args.get('query', '', str)
    page = request.args.get('page', 1, int)
    page_size = request.args.get('pageSize', DEFAULT_PAGE_SIZE, int)
    order_by = request.args.get('orderBy', 'id', str)
    highlights = request.args.get('highlights', False, bool)

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
    return responsify(results), 200


@api.route('course/<int:report_id>')
def get_course(report_id):
    """
    Get a course given its identifier
    """
    report = get_single_course(report_id)
    if not report:
        flask.abort(404)
    else:
        return responsify(report), 200


@api.route('course/<int:report_id>/scores')
def get_scores(report_id):
        """
        Get a course report and scores given its identifier
        """
        report = get_single_report(report_id)
        if not report:
            flask.abort(404)
        else:
            # Avoiding jsonify because it can be slow
            return responsify(report), 200
