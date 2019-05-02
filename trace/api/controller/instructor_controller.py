import flask
from flask import request, jsonify

from api.controller import api
from api.service.instructor_service import get_all_instructors, get_single_instructor, search_instructors, \
        search_highlights_instructors
from api.utils.constants import DEFAULT_PAGE_SIZE
from api.utils.helpers import responsify


@api.route('instructor')
def get_instructors():
        """
        List all instructors
        """
        page = request.args.get('page', 1, int)
        page_size = request.args.get('pageSize', DEFAULT_PAGE_SIZE, int)
        order_by = request.args.get('orderBy', 'id', str)
        term_id = request.args.get('term_id', None, str)
        department_id = request.args.get('department_id', None, str)
        query = request.args.get('query', '', str)
        highlights = request.args.get('highlights', False, bool)

        params = dict(query=query, page=page, page_size=page_size, order_by=order_by, term_id=term_id, department_id=department_id)

        operation = get_all_instructors
        if query:
            operation = search_instructors if not highlights else search_highlights_instructors
            params = {k: v for k, v in params.items() if k not in ['order_by', 'term_id', 'department_id']}
        else:
            params.pop('query')

        results = operation(**params)

        # results = get_all_instructors(page, page_size, order_by, term_id, department_id)
        return responsify(results), 200


@api.route('instructor/<int:instructor_id>')
def get_instructor(instructor_id):
        """
        Get an instructor given its identifier
        """
        instructor = get_single_instructor(instructor_id)
        if not instructor:
            flask.abort(404)
        else:
            return jsonify(instructor), 200
