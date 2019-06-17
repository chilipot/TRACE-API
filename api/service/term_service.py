from api.model import QuestionCategory
from api.model.term import Term
from api.utils.helpers import sort_and_paginate


def get_all_terms(page, page_size, order_by):
    return [t.as_dict() for t in sort_and_paginate(Term.query, order_by, page, page_size).all()]


def get_single_term(term_id):
    result = Term.query.get(term_id)
    return result.as_dict() if result is not None else result


def get_single_term_categories(term_id):
    term_result = Term.query.get(term_id)
    if term_result:
        fields_exclude_override = [field for field in QuestionCategory.exclude_dict_fields if field != 'answers']
        result = [c.as_dict(override_exclude_dict_fields=fields_exclude_override) for c in term_result.categories]
    else:
        result = []
    return result
