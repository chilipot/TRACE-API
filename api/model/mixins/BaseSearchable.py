from elasticsearch_dsl import Search

from api import elasticsearch


class BaseSearchable(object):
    # These should all be defined in a subclass
    INDEX = ''
    ID_FIELD_NAME = ''
    INDEXED_FIELDS = []

    @classmethod
    def _perform_search(cls, expr, page, per_page, facets={}, highlights=False):
        return cls.elastic_search(expr, cls.INDEXED_FIELDS, page, per_page, cls.ID_FIELD_NAME, cls.INDEX, facets=facets,
                                  highlights=highlights)

    @classmethod
    def highlights(cls, expr, page, per_page, facets={}):
        search_result = cls._perform_search(expr, page, per_page, facets=facets, highlights=True)
        # Only select highlights for top 10 search results
        highlights_results = [x.meta for x in search_result[:10] if x.meta.highlight]
        highlights = {field: {} for field in cls.INDEXED_FIELDS}
        for h in highlights_results:
            for key, val in h.highlight.to_dict().items():
                if highlights[key].get(val[0], -1) < h.score:
                    highlights[key][val[0]] = h.score
        for key, val in highlights.items():
            highlights[key] = [pair[0] for pair in sorted(val.items(), key=lambda x: x[1], reverse=True)]
        return highlights

    @classmethod
    def search(cls, expr, page, per_page, facets={}):
        search_result = cls._perform_search(expr, page, per_page, facets=facets, highlights=False)
        ids = [x[cls.ID_FIELD_NAME] for x in search_result]
        return cls.map_all_objects(ids) if ids else []

    @classmethod
    def map_all_objects(cls, ids):
        query_result = cls.query.filter(cls.id.in_(ids)).all()
        object_map = {o.id: o for o in query_result}
        sql_objects = [object_map[obj_id] for obj_id in ids]
        return sql_objects

    @classmethod
    def construct_query(cls, query, _fields_list):
        raise NotImplementedError('Please implement a way to construct an ElasticSearch query for this class')

    @classmethod
    def apply_facets(cls, query, facets):
        for facet in facets.items():
            facet_key, facet_val = facet
            filter_type = 'terms' if isinstance(facet_val, list) else 'term'
            query = query.filter(filter_type, **{facet_key: facet_val})

        return query

    @classmethod
    def elastic_search(cls, query, fields_list, page, per_page, id_field_name, index, facets={}, highlights=False):
        full_query = cls.construct_query(query, fields_list)
        search_query = Search(using=elasticsearch, index=index).query(full_query).source(id_field_name)

        if facets:
            search_query = cls.apply_facets(search_query, facets)

        if highlights:
            for field in fields_list:
                search_query = search_query.highlight(field)

        return search_query[((page - 1) * per_page):(page * per_page)].execute()
