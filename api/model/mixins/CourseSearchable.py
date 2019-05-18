from elasticsearch_dsl.query import MultiMatch

from api.model.mixins.BaseSearchable import BaseSearchable


class CourseSearchable(BaseSearchable):
    INDEX = 'course'
    ID_FIELD_NAME = 'report_id'
    INDEXED_FIELDS = ['course_subject_code', 'course_name', 'instructor_full_name', 'term_title']

    @classmethod
    def construct_query(cls, query, _fields_list):
        fields_list = list(_fields_list)
        # boosts course_subject_code x 2
        fields_list.append(fields_list[fields_list.index('course_subject_code')] + '^2')

        return MultiMatch(query=query, fields=fields_list,
                          type="most_fields", fuzziness='AUTO:6,8', fuzzy_transpositions=True,
                          cutoff_frequency=0.01)
