import flask
from flask import request, jsonify

from api.controller import api
from api.service.department_service import get_all_departments, get_single_department, search_departments, \
        search_highlights_departments
from api.utils.constants import DEFAULT_PAGE_SIZE
from api.utils.helpers import responsify


@api.route('department')
def get_departments():
        """
        List all departments
        """
        page = request.args.get('page', 1, int)
        page_size = request.args.get('pageSize', DEFAULT_PAGE_SIZE, int)
        order_by = request.args.get('orderBy', 'id', str)
        term_id = request.args.get('term_id', None, str)
        query = request.args.get('query', '', str)
        highlights = request.args.get('highlights', False, bool)

        params = dict(query=query, page=page, page_size=page_size, order_by=order_by, term_id=term_id)

        operation = get_all_departments
        if query:
                operation = search_departments if not highlights else search_highlights_departments
                params.pop('term_id')
                params.pop('order_by')
        else:
                params.pop('query')

        results = operation(**params)

        # results = get_all_departments(page, page_size, order_by, term_id)
        return responsify(results), 200


@api.route('department/<int:department_id>')
def get_department(department_id):
        """
        get a department given its identifier
        """
        department = get_single_department(department_id)
        if not department:
            flask.abort(404)
        else:
            return responsify(department), 200
