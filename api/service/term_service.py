from sqlalchemy_utils import sort_query

from api.model.term import Term


def get_all_terms(page, page_size, sort):
    return [t.as_dict() for t in sort_query(Term.query, sort).paginate(page, page_size, False).items]


def get_single_term(term_id):
    result = Term.query.get(term_id)
    return result.as_dict() if result is not None else result
