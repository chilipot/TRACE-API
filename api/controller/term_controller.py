import flask
from flask import request, jsonify

from api.controller import api
from api.service.term_service import get_all_terms, get_single_term
from api.utils.constants import DEFAULT_PAGE_SIZE


@api.route('term')
def get_terms():
        """
        List all terms
        """
        page = request.args.get('page', 1)
        page_size = request.args.get('pageSize', DEFAULT_PAGE_SIZE)
        order_by = request.args.get('orderBy', 'id')
        return jsonify({'data': get_all_terms(page, page_size, order_by)}), 200


@api.route('term/<int:term_id>')
def get_term(term_id):
        """
        get a term given its identifier
        """
        term = get_single_term(term_id)
        if not term:
            flask.abort(404)
        else:
            return jsonify(term), 200
