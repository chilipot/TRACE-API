from elasticsearch_dsl.query import MultiMatch

from api.model.mixins.BaseSearchable import BaseSearchable


class DepartmentSearchable(BaseSearchable):
    INDEXED_FIELDS = ['title', 'code']
    ID_FIELD_NAME = 'department_id'
    INDEX = 'department'

    @classmethod
    def construct_query(cls, query, _fields_list):
        return MultiMatch(query=query, fields=['title', 'code'])
