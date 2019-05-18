from flask import request

from api.controller import api
from api.service.survey_service import get_all_questions
from api.utils.constants import DEFAULT_PAGE_SIZE
from api.utils.helpers import responsify, get_id_facets_from_request


@api.route('question')
def get_questions():
    """
    get list of answerable questions
    """
    page = request.args.get('page', 1)
    page_size = request.args.get('pageSize', DEFAULT_PAGE_SIZE)
    order_by = request.args.get('orderBy', 'id')

    facets = get_id_facets_from_request(['category_id'])

    results = get_all_questions(page, page_size, order_by, facets)

    return responsify(results), 200
