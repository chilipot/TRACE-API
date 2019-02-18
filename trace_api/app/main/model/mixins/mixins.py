from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch
from flask import current_app


class SearchableMixin(object):
    @classmethod
    def search(cls, expr, page, per_page):
        ids = [x['report_id'] for x in elastic_search(expr, page, per_page)]
        if len(ids) == 0:
            return []

        return map_all_courses(cls, ids)


def map_all_courses(cls, ids):
    query_result = cls.query.filter(cls.ReportID.in_(ids)).all()
    object_map = {o.ReportID: o for o in query_result}
    sql_objects = [object_map[obj_id] for obj_id in ids]
    return sql_objects


def elastic_search(query, page, per_page, id_field_name='report_id'):
    match_query = MultiMatch(query=query, fields=['course_title', 'term_title', 'instructor_full_name'],
                             type="most_fields", fuzziness='AUTO:6,8', fuzzy_transpositions=True, cutoff_frequency=0.01)
    search_query = Search(using=current_app.elasticsearch, index='course').query(match_query).source(id_field_name)[
                   ((page - 1) * per_page):(page * per_page)]
    return search_query.execute()
