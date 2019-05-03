from elasticsearch_dsl.query import MultiMatch

from api.model.mixins.BaseSearchable import BaseSearchable


class InstructorSearchable(BaseSearchable):
    INDEX = 'instructor'
    ID_FIELD_NAME = 'instructor_id'
    INDEXED_FIELDS = ['first_name', 'last_name']

    @classmethod
    def construct_query(cls, query, _fields_list):
        print('constructed instructor query')
        return MultiMatch(query=query, fields=_fields_list,
                          type="cross_fields", minimum_should_match='50%')
