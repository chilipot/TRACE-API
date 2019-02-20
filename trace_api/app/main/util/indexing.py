from functools import reduce

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch, Match, Q
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.main import db, create_app
from app.main.model.tables import Report, Instructor, Term

from pprint import pprint as pp


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch("https://search-trace-api-jxs4od347kkmjnzstpobjwth64.us-east-2.es.amazonaws.com/")
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
            "number_of_replicas": 0
        },
        "mappings": {
            "courses": {
                "dynamic": "strict",
                "properties": {
                    "course_title": {
                        "type": "text"
                    },
                    "term_title": {
                        "type": "text"
                    },
                    "instructor_full_name": {
                        "type": "text"
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
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def store_record(elastic_object, index_name, record):
    try:
        outcome = elastic_object.index(index=index_name, doc_type='courses', body=record)
    except Exception as ex:
        print('Error in indexing data')
        print(str(ex))
    return outcome


def set_props_index_obj(item):
    return {
        "course_title": item.course_full_name.strip(),
        "term_title": item.Term.normal_title.strip(),
        "instructor_full_name": item.Instructor.full_name.strip(),
        "report_id": item.ReportID
    }


def index_all_courses(elastic_object, index_name):
    results = Report.query.join(Report.Term).join(Report.Instructor).all()
    index_objs = [set_props_index_obj(result) for result in results]
    for index_obj in index_objs:
        store_record(elastic_object, index_name, index_obj)


def map_all_courses(ids):
    query_result = Report.query.filter(Report.ReportID.in_(ids)).join(Report.Term).join(Report.Instructor).all()
    object_map = {o.ReportID: o for o in query_result}
    sql_objects = [object_map[obj_id] for obj_id in ids]
    return sql_objects


def elasticsearch(query, page, per_page):
    match_query = MultiMatch(query=query, fields=['course_title', 'term_title', 'instructor_full_name'],
                             type="most_fields", fuzziness='AUTO:6,8', fuzzy_transpositions=True, cutoff_frequency=0.01)
    search_query = Search(using=es, index='course').query(match_query).source("report_id")[page: page * per_page]
    return search_query.execute()


def get_all_course_names():
    return Report.query.all()


def get_all_instructor_names():
    return Instructor.query.all()


def get_all_term_titles():
    return Term.query.all()


if __name__ == "__main__":
    es = connect_elasticsearch()
    # new_index = create_index(es, "course")
    #
    app = create_app('dev')
    app.app_context().push()
    manager = Manager(app)
    migrate = Migrate(app, db)
    manager.add_command('db', MigrateCommand)

    # import random
    #
    # course_names = {' '.join(random.sample(x.split(" "), len(x.split(" ")))).lower(): 'course' for x in
    #                 set(r.course_full_name for r in get_all_course_names())}
    # instructor_names = {' '.join(random.sample(x.split(" "), len(x.split(" ")))).lower(): 'instructor' for x in
    #                     set(r.full_name for r in get_all_instructor_names())}
    # term_titles = {' '.join(random.sample(x.split(" "), len(x.split(" ")))).lower(): 'term' for x in
    #                set(r.normal_title for r in get_all_term_titles())}
    #
    # entity_lookup = {**course_names, **instructor_names}
    # entity_lookup = {**entity_lookup, **term_titles}
    #
    # data_objs = []
    # for i in range(0, 8000):
    #     entities = [random.sample(course_names.keys(), 1)[0], random.sample(instructor_names.keys(), 1)[0],
    #                 random.sample(term_titles.keys(), 1)[0]]
    #     random.shuffle(entities)
    #     search_str = ' '.join(entities)
    #     classifications = [{"start": search_str.index(entity), "end": search_str.index(entity) + len(entity),
    #                         "label": entity_lookup.get(entity), "text": entity} for entity in entities]
    #     data_obj = [search_str, classifications]
    #     data_objs.append(data_obj)
    #     print(str(i))
    #
    # import json
    # with open("model_data_temp.txt", "w") as f:
    #     json.dump(data_objs, f)


    # index_all_courses(es, "course")
    # results_page = elasticsearch("engw 1111 westhuges", 1, 25)
    # pp(results_page)
    #
    # sql_results = map_all_courses([x['report_id'] for x in results_page])
    # pp(sql_results)
