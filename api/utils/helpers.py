import json
import os

from flask import request
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


def responsify(results, status):
    results_obj = {}
    if isinstance(results, dict):
        results_obj = results
    elif isinstance(results, list) or isinstance(results, str):
        results_obj = {"data": results}
    return {'statusCode': status,
            "isBase64Encoded": False,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
            'body': json.dumps(results_obj)}

class Abort(Exception):
    
    def __init__(self, code, reason):
        msg = f"ERROR:{code} MSG: {reason}"
        super(Abort, self).__init__(msg)

class Serverless:
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    args = {}

    class Args(object):
        def __init__(self, parameters={}):
            self.params = parameters

        def get(self, key, default, type):
            try:
                value = self.params.get(key)
                if value:
                    return type(value)
                else:
                    return default
            except TypeError:
                raise Abort(400, f"{type} is not a valid Type")
            except ValueError:
                return Abort(400, f"Invalid literal {key} for type {type}")

    @classmethod
    def lambda_handler(cls, event, context):
        cls.logger.info('## ENVIRONMENT VARIABLES')
        cls.logger.info(os.environ)
        cls.logger.info('## EVENT')
        cls.logger.info(event)

    @classmethod
    def route(cls, func):
        def wrapper(event: dict, context):
            cls.lambda_handler(event, context)
            stringParams: dict = event.get('queryStringParameters') or {}
            pathParams: dict = event.get('pathParameters') or {}
            cls.args = cls.Args(stringParams)

            cls.logger.info(f"Arguments {stringParams} | {pathParams}")

            try:
                return func(pathParams) if pathParams else func()
            except Exception as e:
                return responsify(f"An unknown error occurred {e}", 400)

        return wrapper

    @staticmethod
    def abort(code=500, reason="Request was abruptly aborted"):
        raise Abort(code, reason)
