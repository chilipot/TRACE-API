from flask import json, Response, request, abort
from sqlalchemy_utils import sort_query


def get_id_facets_from_request(facet_keys):
    return {k: v for k, v in {fk: request.args.get(fk, '').split(',') for fk in facet_keys}.items()
            if v != [] and v != ['']}


def apply_sql_facets(cls, query, facets):
    def get_sql_facet(facet):
        facet_key, facet_val = facet
        multi_match = isinstance(facet_val, list)
        if multi_match and len(facet_val) > 1:
            return getattr(cls, facet_key).in_(facet_val)
        else:
            return getattr(cls, facet_key) == (facet_val if not multi_match else facet_val[0])

    filters = set(get_sql_facet(facet) for facet in facets.items())
    return query.filter(*filters)


def sort_and_paginate(query, order_by, _page, page_size):
    page = _page - 1
    return sort_query(query, order_by).slice(page * page_size, page_size + (page * page_size))


def responsify(results):
    results_obj = {}
    if isinstance(results, dict):
        results_obj = results
    elif isinstance(results, list):
        results_obj = {"data": results}
    return Response(json.dumps(results_obj), mimetype='application/json')


def get_or_abort(model, object_id, code=404):
    """
    get an object with his given id or an abort error (404 is the default)
    """
    result = model.query.get(object_id)
    if result is None:
        abort(code)
    return result
