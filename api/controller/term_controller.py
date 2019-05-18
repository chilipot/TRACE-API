from api.service.term_service import get_all_terms, get_single_term
from api.utils.constants import DEFAULT_PAGE_SIZE
from api.utils.helpers import responsify, Serverless


@Serverless.route
def get_terms():
    """
    List all terms
    """
    page = Serverless.args.get('page', 1, int)
    page_size = Serverless.args.get('pageSize', DEFAULT_PAGE_SIZE, int)
    order_by = Serverless.args.get('orderBy', 'id', str)

    results = get_all_terms(page, page_size, order_by)
    return responsify(results, 200)


@Serverless.route
def get_term(term_id):
    """
    get a term given its identifier
    """
    term = get_single_term(term_id)
    if term:
        return responsify(term, 200)
    else:
        return Serverless.abort(404)

