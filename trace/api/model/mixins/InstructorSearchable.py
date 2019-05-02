from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch
from flask import current_app

INDEXED_FIELDS = ['first_name', 'last_name']


class InstructorSearchable(object):
    @classmethod
    def _perform_search(cls, expr, page, per_page, highlights=False):
        return cls.elastic_search(expr, INDEXED_FIELDS, page, per_page, highlights=highlights)

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
    def search(cls, expr, page, per_page):
        search_result = cls._perform_search(expr, page, per_page, highlights=False)
        ids = [x['instructor_id'] for x in search_result]
        return cls.map_all_instructors(ids) if ids else []

    @classmethod
    def map_all_instructors(cls, ids):
        query_result = cls.query.filter(cls.id.in_(ids)).all()
        object_map = {o.id: o for o in query_result}
        sql_objects = [object_map[obj_id] for obj_id in ids]
        return sql_objects

    @classmethod
    def construct_query(cls, query, _fields_list):
        match_query = MultiMatch(query=query, fields=_fields_list,
                                 type="cross_fields", minimum_should_match='50%')
        return match_query

    @classmethod
    def elastic_search(cls, query, fields_list, page, per_page, id_field_name='instructor_id', highlights=False,
                       index='instructor'):
        full_query = cls.construct_query(query, fields_list)
        search_query = Search(using=current_app.elasticsearch, index=index).query(full_query).source(id_field_name)
        if highlights:
            for field in fields_list:
                search_query = search_query.highlight(field)

        return search_query[((page - 1) * per_page):(page * per_page)].execute()
