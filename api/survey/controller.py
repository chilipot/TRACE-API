from api.survey.service import get_all_questions, get_all_categories
from api.utils.constants import DEFAULT_PAGE_SIZE
from api.utils.helpers import get_id_facets_from_request, Serverless


@Serverless.route
def get_questions():
    """
    get list of answerable questions
    """
    page = Serverless.args.get('page', 1)
    page_size = Serverless.args.get('pageSize', DEFAULT_PAGE_SIZE)
    order_by = Serverless.args.get('orderBy', 'id')

    facets = get_id_facets_from_request(['category_id'])

    results = get_all_questions(page, page_size, order_by, facets)

    return results, 200


@Serverless.route
def get_categories():
    """
    get list of answerable questions
    """
    page = Serverless.args.get('page', 1)
    page_size = Serverless.args.get('pageSize', DEFAULT_PAGE_SIZE)
    order_by = Serverless.args.get('orderBy', 'id')

    results = get_all_categories(page, page_size, order_by)

    return results, 200
