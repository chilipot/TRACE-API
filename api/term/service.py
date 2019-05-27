from api.model.term import Term
from api.utils.helpers import sort_and_paginate


def get_all_terms(page, page_size, order_by):
    return (t.as_dict() for t in sort_and_paginate(Term.query, order_by, page, page_size).all())


def get_single_term(term_id):
    result = Term.query.get(term_id)
    return result.as_dict() if result is not None else result
