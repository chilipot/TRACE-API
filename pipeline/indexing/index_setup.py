import json

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch

from api import create_app
from api.model.course import Course
from api.model.instructor import Instructor
from api.model.term import Term


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch(
        "https://search-nutrace-q4krcpst6ceoktoppbgbvgrjyy.us-east-1.es.amazonaws.com/")
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es


def create_index(es_object, index_name='course'):
    created = False
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "analyzer": {
                    "std_english_analyzer": {
                        "type": "standard",
                        "stopwords": "_english_"
                    }
                }
            }
        },
        "mappings": {
            "courses": {
                "dynamic": "strict",
                "properties": {
                    "course_name": {
                        "type": "text",
                        "search_analyzer": "english",
                        "analyzer": "english"
                    },
                    "course_subject_code": {
                        "type": "text",
                    },
                    "term_title": {
                        "type": "text",
                    },
                    "instructor_full_name": {
                        "type": "text",
                    },
                    "report_id": {
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


def store_record(elastic_object, index_name, record):
    try:
        outcome = elastic_object.index(index=index_name, doc_type='courses',
                                       body=record)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))
    return outcome


def set_props_index_obj(item):
    return {
        "course_name": item.name.strip(),
        "course_subject_code": f'{item.subject} {item.number}',
        "term_title": item.term.normal_title.strip(),
        "instructor_full_name": item.instructor.full_name.strip(),
        "report_id": item.id
    }


def index_all_courses(elastic_object, index_name):
    results = Course.query.join(Course.term).join(Course.instructor).all()
    index_objs = [set_props_index_obj(result) for result in results]
    for index_obj in index_objs:
        store_record(elastic_object, index_name, index_obj)


def map_all_courses(ids):
    query_result = Course.query.filter(Course.id.in_(ids)).join(
        Course.term).join(Course.instructor).all()
    object_map = {o.id: o for o in query_result}
    sql_objects = [object_map[obj_id] for obj_id in ids]
    return sql_objects


def elasticsearch(es, query, page=1, per_page=25):
    match_query = MultiMatch(query=query, fields=['course_name', 'course_subject_code^2', 'term_title',
                                                  'instructor_full_name'],
                             type="most_fields", fuzziness='AUTO:6,8',
                             fuzzy_transpositions=True, cutoff_frequency=0.01)
    search_query = Search(using=es, index='course').query(match_query)[page: page * per_page]
    return search_query.execute()


def get_all_course_names():
    return Course.query.all()


def get_all_instructor_names():
    return Instructor.query.all()


def get_all_term_titles():
    return Term.query.all()


if __name__ == '__main__':
    app = create_app('dev')
    app.app_context().push()
    es = connect_elasticsearch()
    # es.indices.delete(index='course', ignore=[400, 404])
    # create_index(es)
    # index_all_courses(es, 'course')
    result = elasticsearch(es, 'fundamentals the ben lerner')
    # print(json.dumps(result.meta.explanation.__dict__))
    result_objs = map_all_courses([x['report_id'] for x in result])
    print(json.dumps([x.as_dict() for x in result_objs]))
