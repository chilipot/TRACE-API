from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch, Q
from flask import current_app
from sqlalchemy.orm import contains_eager

INDEXED_FIELDS = ['course_subject_code', 'course_name', 'instructor_full_name', 'term_title']


class CourseSearchable(object):
    @classmethod
    def _perform_search(cls, expr, page, per_page, highlights=False):
        return cls.elastic_search(expr, INDEXED_FIELDS, page, per_page, highlights=highlights)

    @classmethod
    def search(cls, expr, page, per_page):
        search_result = cls._perform_search(expr, page, per_page, highlights=False)
        ids = [x['report_id'] for x in search_result]
        return cls.map_all_courses(ids) if ids else []

    @classmethod
    def highlights(cls, expr, page, per_page):
        search_result = cls._perform_search(expr, page, per_page, highlights=True)
        # Only select highlights for top 10 search results
        highlights_results = [x.meta for x in search_result[:10] if x.meta.highlight]
        highlights = {field: {} for field in INDEXED_FIELDS}
        for h in highlights_results:
            for key, val in h.highlight.to_dict().items():
                if highlights[key].get(val[0], -1) < h.score:
                    highlights[key][val[0]] = h.score
        for key, val in highlights.items():
            highlights[key] = [pair[0] for pair in sorted(val.items(), key=lambda x: x[1], reverse=True)]
        return highlights

    @classmethod
    def map_all_courses(cls, ids):
        query_result = cls.query.filter(cls.id.in_(ids)).join(cls.term).join(cls.instructor).options(
            contains_eager(cls.term)).options(contains_eager(cls.instructor)).all()
        object_map = {o.id: o for o in query_result}
        sql_objects = [object_map[obj_id] for obj_id in ids]
        return sql_objects

    @classmethod
    def construct_query(cls, query, _fields_list):
        fields_list = list(_fields_list)
        # boosts course_subject_code x 2
        fields_list.append(fields_list[fields_list.index('course_subject_code')] + '^2')

        match_query = Q(MultiMatch(query=query, fields=fields_list,
                                   type="most_fields", fuzziness='AUTO:6,8', fuzzy_transpositions=True,
                                   cutoff_frequency=0.01))
        return match_query

    @classmethod
    def elastic_search(cls, query, fields_list, page, per_page, id_field_name='report_id', highlights=False):
        full_query = cls.construct_query(query, fields_list)
        search_query = Search(using=current_app.elasticsearch, index='course').query(full_query).source(id_field_name)
        if highlights:
            for field in fields_list:
                search_query = search_query.highlight(field)

        return search_query[((page - 1) * per_page):(page * per_page)].execute()
