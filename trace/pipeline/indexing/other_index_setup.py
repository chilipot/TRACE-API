import json

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch

from api import create_app
from api.model.instructor import Instructor


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch(
        "https://search-nutrace-q4krcpst6ceoktoppbgbvgrjyy.us-east-1.es.amazonaws.com/")
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es


def create_instructor_index(es_object, index_name='instructor'):
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
            "instructors": {
                "dynamic": "strict",
                "properties": {
                    "first_name": {
                        "type": "text",
                        "analyzer": "autocomplete",
                        "search_analyzer": "standard"
                    },
                    "last_name": {
                        "type": "text",
                        "analyzer": "autocomplete",
                        "search_analyzer": "standard"
                    },
                    "instructor_id": {
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


def set_props_index_obj_inst(item):
    return {
        "first_name": item.first_name,
        "last_name": item.last_name,
        "instructor_id": item.id
    }


def index_all_instructors(elastic_object, index_name):
    results = Instructor.query.all()
    index_objs = [set_props_index_obj_inst(res) for res in results]
    for index_obj in index_objs:
        store_record(elastic_object, index_name, index_obj, 'instructors')


def map_all_instructors(ids):
    query_result = Instructor.query.filter(Instructor.id.in_(ids)).all()
    object_map = {o.id: o for o in query_result}
    sql_objects = [object_map[obj_id] for obj_id in ids]
    return sql_objects


def elasticsearch(es, query, page=0, per_page=25):
    match_query = MultiMatch(query=query, fields=['first_name', 'last_name'],
                             type="cross_fields", minimum_should_match='50%')
    search_query = Search(using=es, index='instructor').query(match_query)[page:(page+1)*per_page]
    return search_query.execute()


if __name__ == '__main__':
    app = create_app('dev')
    app.app_context().push()
    es = connect_elasticsearch()
    # es.indices.delete(index='instructor', ignore=[400, 404])
    # create_instructor_index(es)
    # index_all_instructors(es, 'instructor')
    result = elasticsearch(es, 'wes dura')
    # print(json.dumps(result.meta.explanation.__dict__))
    result_objs = map_all_instructors([x['instructor_id'] for x in result])
    print(json.dumps([x.as_dict() for x in result_objs]))

