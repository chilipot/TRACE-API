from functools import reduce

from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch, Q, Match
from flask import current_app, session
from sqlalchemy.orm import contains_eager


class SearchableMixin(object):
    @classmethod
    def search(cls, expr, page, per_page):
        optimized_query, instructor = get_instructor_from_query(expr)
        course_search, term = get_term_from_query(optimized_query)
        ids = [x['report_id'] for x in
               elastic_search(course_search, instructor, term, page, per_page)]
        return map_all_courses(cls, ids) if len(ids) > 0 else []


def get_term_from_query(query):
    def check_term_presence(term):
        checks = [word.lower() in query.lower().split(" ") for word in
                  term.split(" ")]
        return checks and all(checks)

    found_terms = sorted(
        filter(check_term_presence, session.get('cached_terms', [])),
        key=lambda t: len(t))
    return pop_phrase_from_query(query, found_terms[0] if len(
        found_terms) > 0 else None)


def get_instructor_from_query(query):
    if 'instructor_names' not in session:
        session['instructor_names'] = []
    session_found_name = next(
        [name for name in set(session.get('instructor_names', set())) if
         name in query].__iter__(),
        None)

    if session_found_name is not None:
        entity = session_found_name
    else:
        pldots = current_app.paralleldots
        result = pldots.ner(query)
        # result = {"entities": [{"name": "benjamin lerner"}]} # Debug
        entities = [e['name'] for e in result['entities']]
        entity = entities[0] if len(entities) > 0 else None
        if len(entities) > 0 and entities[0] not in set(
                session.get('instructor_names')):
            session.get('instructor_names').append(entities[0])
            session.modified = True
    return pop_phrase_from_query(query, entity, case_sensitive=True)


def pop_phrase_from_query(query, phrase, case_sensitive=False):
    if phrase is not None:
        ind = query.index(phrase) if case_sensitive else query.lower().index(
            phrase.lower())
        new_query = (query[0:ind] + query[ind + len(phrase):]).replace('  ',
                                                                       ' ')
        return new_query, phrase
    else:
        return query, None


def map_all_courses(cls, ids):
    query_result = cls.query.filter(cls.ReportID.in_(ids)).join(cls.Term).join(
        cls.Instructor).options(
        contains_eager(cls.Term)).options(contains_eager(cls.Instructor)).all()
    object_map = {o.ReportID: o for o in query_result}
    sql_objects = [object_map[obj_id] for obj_id in ids]
    return sql_objects


def construct_query(query, instructor_search, term_search):
    fields_list = ['course_title', 'term_title', 'instructor_full_name']

    queries = []
    # full_query = match_query
    if instructor_search is not None:
        fields_list.remove('instructor_full_name')
        instructor_query = Q(
            Match(instructor_full_name={'query': instructor_search,
                                        'fuzziness': 'AUTO:5,7',
                                        'fuzzy_transpositions': True}))

        queries.append(instructor_query)

    if term_search is not None:
        fields_list.remove('term_title')

        term_query = Q(
            Match(term_title={'query': term_search}))

        queries.append(term_query)

    if len(fields_list) > 1:
        match_query = Q(MultiMatch(query=query, fields=fields_list,
                                   type="most_fields", fuzziness='AUTO:6,8',
                                   fuzzy_transpositions=True,
                                   cutoff_frequency=0.01))
    else:
        match_query = Q(
            Match(course_title={'query': query, 'fuzziness': 'AUTO:6,8',
                                'fuzzy_transpositions': True}))
    if query and query.strip():
        queries.append(match_query)

    full_query = reduce(lambda q1, q2: q1 | q2, queries)
    return full_query


def elastic_search(query, instructor_search, term_search, page, per_page,
                   id_field_name='report_id'):
    full_query = construct_query(query, instructor_search, term_search)
    search_query = Search(using=current_app.elasticsearch,
                          index='course').query(full_query).source(
        id_field_name)[
                   ((page - 1) * per_page):(page * per_page)]
    return search_query.execute()
