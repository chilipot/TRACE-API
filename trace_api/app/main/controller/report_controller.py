from flask_restplus import Resource

from ..service.report_service import get_all_terms, get_term, get_all_instructors, get_instructor, \
    get_all_course_reports, get_course_report, search_course_reports
from ..util.dto import ReportDto

api = ReportDto.api
_term = ReportDto.term
_instructor = ReportDto.instructor
_course = ReportDto.course

pagination_parser = api.parser()
pagination_parser.add_argument('page', type=int, help='Page Number')
pagination_parser.add_argument('pageSize', type=int, help='Size of Single Page')

list_args_parser = pagination_parser.copy()
list_args_parser.add_argument('orderBy', type=str, help='Expression to order by. In format <property> for ascending,'
                                                        + ' -<property> for descending, and <parent_prop>-<child_prop>'
                                                        + ' to sort by a child property ascending or descending.'
                                                        + ' Ignored if "q" has a value (searching), where order will be'
                                                        + ' by search relevance.')

search_args_parser = list_args_parser.copy()
search_args_parser.add_argument('q', type=str, help='Expression to search with')

DEFAULT_PAGE_SIZE = 25


@api.route('term')
@api.expect(list_args_parser)
class TermList(Resource):
    @api.doc('list_of_terms')
    @api.marshal_list_with(_term, envelope='data')
    def get(self):
        """
        List all terms
        """
        args = list_args_parser.parse_args()
        page = args.get('page') or 1
        page_size = args.get('pageSize') or DEFAULT_PAGE_SIZE
        order_by = args.get('orderBy') or 'TermID'
        return get_all_terms(page, page_size, order_by)


@api.route('term/<term_id>')
@api.param('term_id', 'The Term identifier')
@api.response(404, 'Term not found.')
class Term(Resource):
    @api.doc('get a term')
    @api.marshal_with(_term)
    def get(self, term_id):
        """
        get a term given its identifier
        """
        term = get_term(term_id)
        if not term:
            api.abort(404)
        else:
            return term


@api.route('instructor')
@api.expect(list_args_parser)
class InstructorList(Resource):
    @api.doc('list_of_instructors')
    @api.marshal_list_with(_instructor, envelope='data')
    def get(self):
        """
        List all instructors
        """
        args = list_args_parser.parse_args()
        page = args.get('page') or 1
        page_size = args.get('pageSize') or DEFAULT_PAGE_SIZE
        order_by = args.get('orderBy', 'InstructorID') or 'InstructorID'
        return get_all_instructors(page, page_size, order_by)


@api.route('instructor/<instructor_id>')
@api.param('instructor_id', 'The instructor identifier')
@api.response(404, 'instructor not found.')
class Instructor(Resource):
    @api.doc('get a instructor')
    @api.marshal_with(_instructor)
    def get(self, instructor_id):
        """
        get an instructor given its identifier
        """
        instructor = get_instructor(instructor_id)
        if not instructor:
            api.abort(404)
        else:
            return instructor


@api.route('report')
@api.expect(search_args_parser)
class CourseReportList(Resource):
    @api.doc('list_of_reports')
    @api.marshal_list_with(_course, envelope='data')
    def get(self):
        """
        List many reports
        """
        args = search_args_parser.parse_args()
        query = args.get('q') or ''
        page = args.get('page') or 1
        page_size = args.get('pageSize') or DEFAULT_PAGE_SIZE
        order_by = args.get('orderBy') or 'ReportID'
        if query:
            return search_course_reports(query, page, page_size)
        else:
            return get_all_course_reports(page, page_size, order_by)


@api.route('report/<report_id>')
@api.param('report_id', 'The Course Report identifier')
@api.response(404, 'report not found.')
class CourseReport(Resource):
    @api.doc('get a report')
    @api.marshal_with(_course)
    def get(self, report_id):
        """
        get a report given its identifier
        """
        report = get_course_report(report_id)
        if not report:
            api.abort(404)
        else:
            return report
