import json

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch, Match, Q

from api import create_app, db_session
from api.model.department import Department
from api.model.instructor import Instructor


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch(
        "https://vpc-nu-trace-b7xszvmk2oxocak5pwp6n4d4yy.us-east-1.es.amazonaws.com/")
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es


def create_department_index(es_object, index_name='department'):
    created = False
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "filter": {
                    "autocomplete_filter": {
                        "type": "edge_ngram",
                        "min_gram": 1,
                        "max_gram": 20
                    }
                },
                "analyzer": {
                    "autocomplete": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "autocomplete_filter"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "departments": {
                "dynamic": "strict",
                "properties": {
                    "title": {
                        "type": "text",
                        "analyzer": "autocomplete",
                        "search_analyzer": "english"
                    },
                    "code": {
                        "type": "text"
                    },
                    "department_id": {
                        "type": "integer"
                    }
                }
            }
        }
    }

    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400,
                                     body=settings)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def store_record(elastic_object, index_name, record, doc_type):
    try:
        outcome = elastic_object.index(index=index_name, doc_type=doc_type,
                                       body=record)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))
    return outcome


def set_props_index_obj_dept(item):
    return {
        "title": item.title,
        "code": item.code,
        "department_id": item.id
    }


def index_all_departments(elastic_object, index_name):
    results = Department.query.all()
    index_objs = [set_props_index_obj_dept(res) for res in results]
    for index_obj in index_objs:
        store_record(elastic_object, index_name, index_obj, 'departments')


def map_all_departments(ids):
    query_result = Department.query.filter(Department.id.in_(ids)).all()
    object_map = {o.id: o for o in query_result}
    sql_objects = [object_map[obj_id] for obj_id in ids]
    return sql_objects


def elasticsearch(es, query, page=0, per_page=25):
    match_query = MultiMatch(query=query, fields=['title', 'code'])
    search_query = Search(using=es, index='department').query(match_query)[page:(page+1)*per_page]
    return search_query.execute()


if __name__ == '__main__':
    db_sess = db_session
    # app = create_app('dev')
    # app.app_context().push()
    es = connect_elasticsearch()
    # es.indices.delete(index='department', ignore=[400, 404])
    # create_department_index(es)
    # index_all_departments(es, 'department')
    result = elasticsearch(es, 'heal sci')
    # print(json.dumps(result.meta.explanation.__dict__))
    result_objs = map_all_departments([x['department_id'] for x in result])
    print(json.dumps([x.as_dict() for x in result_objs]))

