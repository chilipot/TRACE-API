from api.model import LookupQuestion, QuestionCategory
from api.utils.helpers import sort_and_paginate, apply_sql_facets


def get_all_questions(page, page_size, order_by, facets={}):
    query = LookupQuestion.query
    if facets:
        query = apply_sql_facets(LookupQuestion, query, facets)
    return [q.as_dict() for q in sort_and_paginate(query, order_by, page, page_size).all()]


def get_all_categories(page, page_size, order_by):
    fields_exclude_override = [field for field in QuestionCategory.exclude_dict_fields if field != 'answers']
    return [c.as_dict(override_exclude_dict_fields=fields_exclude_override) for c in
            sort_and_paginate(QuestionCategory.query, order_by, page, page_size).all()]
