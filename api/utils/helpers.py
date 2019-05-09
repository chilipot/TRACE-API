from flask import json, Response
from sqlalchemy_utils import sort_query


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
