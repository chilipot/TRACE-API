import flask
from flask import request, jsonify

from api.controller import api
from api.service.department_service import get_all_departments, get_single_department
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

        results = get_all_departments(page, page_size, order_by, term_id)
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
            return jsonify(department), 200
