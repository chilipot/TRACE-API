from api.model import LookupQuestion
from api.utils.helpers import sort_and_paginate, apply_sql_facets


def get_all_questions(page, page_size, order_by, facets={}):
    query = LookupQuestion.query
    if facets:
        query = apply_sql_facets(LookupQuestion, query, facets)
    return [q.as_dict() for q in sort_and_paginate(query, order_by, page, page_size).all()]
