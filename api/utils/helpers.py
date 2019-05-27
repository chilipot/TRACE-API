import json
import os
import logging

from sqlalchemy_utils import sort_query


def responsify(body, code, headers=None):
    default_headers = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Credentials": True}
    default_headers.update(headers) if headers else None

    results_obj = {}
    if isinstance(body, dict):
        results_obj = body
    elif isinstance(body, list) or isinstance(body, str):
        results_obj = {"data": body}
    return {
        'statusCode': code,
        "isBase64Encoded": False,
        'headers': default_headers,
        'body': json.dumps(results_obj)
    }


class Abort(Exception):
    def __init__(self, code, reason):
        msg = f"ERROR:{code} MSG: {reason}"
        super(Abort, self).__init__(msg)


class Serverless:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    args = {}

    class Args(object):
        def __init__(self, parameters={}):
            self.params = parameters

        def get(self, key, default, type=str):
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
    def lambda_handler(cls, event):
        cls.logger.info('## ENVIRONMENT VARIABLES')
        cls.logger.info(os.environ)
        cls.logger.info('## EVENT')
        cls.logger.info(event)

    @classmethod
    def route(cls, func):
        def wrapper(event: dict, _):
            cls.lambda_handler(event)
            stringParams: dict = event.get('queryStringParameters') or {}
            pathParams: dict = event.get('pathParameters') or {}
            cls.args = cls.Args(stringParams)

            cls.logger.info(f"Arguments {stringParams} | {pathParams}")

            try:
                body, *context = func(pathParams) if pathParams else func()
                code, headers = context if len(context) > 1 else (context[0], None)
                res = responsify(body, code, headers)
                cls.logger.info(res)
                return res
            except Exception as e:
                return responsify(f"An unknown error occurred {e}", 400)

        return wrapper

    @staticmethod
    def abort(code=500, reason="Request was abruptly aborted"):
        raise Abort(code, reason)


def get_id_facets_from_request(facet_keys):
    return {k: v for k, v in {fk: Serverless.args.get(fk, '').split(',') for fk in facet_keys}.items()
            if v != [] and v != ['']}


def apply_sql_facets(cls, query, facets):
    def get_sql_facet(facet):
        facet_key, facet_val = facet
        multi_match = isinstance(facet_val, list)
        if multi_match and len(facet_val) > 1:
            return getattr(cls, facet_key).in_(facet_val)
        else:
            return getattr(cls, facet_key) == (facet_val if not multi_match else facet_val[0])

    filters = {get_sql_facet(facet) for facet in facets.items()}
    return query.filter(*filters)


def sort_and_paginate(query, order_by, _page, page_size):
    page = _page - 1
    return sort_query(query, order_by).slice(page * page_size, page_size + (page * page_size))
