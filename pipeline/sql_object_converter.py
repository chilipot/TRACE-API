import csv
import json

from pipeline.complex_json_encoder import ComplexJSONSerializable, ComplexEncoder
import pipeline.trace as trace


class IDNameRetriever:
    def get_id_name(self):
        return None


class Comment(ComplexJSONSerializable, IDNameRetriever):
    def __init__(self, commentID, text, report_id):
        self.commentID = commentID
        self.text = text
        self.report_id = report_id

    def get_id_name(self):
        return "commentID"


class Instructor(ComplexJSONSerializable, IDNameRetriever):
    def __init__(self, instructorID, firstName, middleName, lastName):
        self.instructorID = instructorID
        self.firstName = firstName
        self.middleName = middleName
        self.lastName = lastName

    def get_id_name(self):
        return "instructorID"


class Term(ComplexJSONSerializable, IDNameRetriever):
    def __init__(self, termID, title):
        self.termID = termID
        self.title = title

    def get_id_name(self):
        return "termID"


class Department(ComplexJSONSerializable, IDNameRetriever):
    def __init__(self, departmentID, code, title):
        self.departmentID = departmentID
        self.code = code
        self.title = title

    def get_id_name(self):
        return "departmentID"


class Course(ComplexJSONSerializable, IDNameRetriever):
    def __init__(self, id, report_id, instructorID, termID, name, subject, number, section, crn, departmentID):
        self.courseID = id
        self.instructorID = instructorID
        self.termID = termID
        self.departmentID = departmentID
        self.name = name
        self.subject = subject
        self.number = number
        self.section = section
        self.report_id = report_id
        self.crn = crn

    # self.dataID = dataID

    def get_id_name(self):
        return "courseID"


class Lookup_QuestionText(ComplexJSONSerializable, IDNameRetriever):
    def __init__(self, abbrev, text, questionTextID):
        self.abbrev = abbrev
        self.text = text
        self.questionTextID = questionTextID

    def get_id_name(self):
        return "questionTextID"


class Lookup_AnswerText(ComplexJSONSerializable, IDNameRetriever):
    def __init__(self, text, answerTextID):
        self.text = text
        self.answerTextID = answerTextID

    def get_id_name(self):
        return "answerTextID"


class Answer(ComplexJSONSerializable, IDNameRetriever):
    def __init__(self, answerID, answerTextID, questionID, value):
        self.answerTextID = answerTextID
        self.answerID = answerID
        self.questionID = questionID
        self.value = value

    def get_id_name(self):
        return "answerID"


class Question(ComplexJSONSerializable, IDNameRetriever):
    def __init__(self, questionID, legacyID, respCount, respRate, mean, median, stdDev, questionTextID, dataID):
        self.respCount = respCount
        self.respRate = respRate
        self.mean = mean
        self.median = median
        self.stdDev = stdDev
        self.questionTextID = questionTextID
        self.dataID = dataID
        self.questionID = questionID
        self.legacyID = legacyID

    def get_id_name(self):
        return "questionID"


class ScoreData(ComplexJSONSerializable, IDNameRetriever):
    def __init__(self, dataID, reportID, enrollment, responses, declines):
        self.dataID = dataID
        # self.legacyMongoID = legacyMongoID
        self.reportID = reportID
        self.enrollment = enrollment
        self.responses = responses
        self.declines = declines

    def get_id_name(self):
        return "dataID"


def get_all_reports(run_pipeline=False):
    reports = []
    if not run_pipeline:
        with open("data/full_data.json") as f:
            reports = json.load(f)
            for ind, report in enumerate(reports):
                report['report_id'] = ind + 1
    else:
        reports = trace.get_all_reports()

    return reports


def get_all_scores(reports):
    scores = []

    for report in reports:
        scores += [report['data']]

    return scores


def find_first(items, pred, default=None):
    return next((i for i in items if pred(i)), default)


def make_unique_json(obj_list):
    json_list = []
    if len(obj_list) > 0:
        type_name = type(obj_list[0]).__name__
        json_list = list(json.loads(objStr) for objStr in set(json.dumps(
            el, sort_keys=True, cls=ComplexEncoder, ensure_ascii=False) for el in obj_list))
        # json_list = list(np.unique(list(np.array(json_list))))

        print("Before - " + type_name + " : " + str(len(obj_list)))
        print("After - " + type_name + " : " + str(len(json_list)))

    for ind, jobj in enumerate(json_list):
        id_name = obj_list[0].get_id_name()
        jobj[id_name] = ind + 1 if jobj[id_name] == 0 else jobj[id_name]

    return json_list


def get_lookup_questiontexts(reports):
    questionTexts = []
    for report in reports:
        for question in (report['data'][1:] if len(report['data']) > 1 else []):
            questionTexts += [Lookup_QuestionText(
                question['Question Abbrev'], question['Question Text'], 0)]

    return questionTexts


def get_lookup_answertexts(reports):
    answerTexts = set()
    for report in reports:
        for question in (report['data'][1:] if len(report['data']) > 1 else []):
            answerTexts |= set(key for key in question.keys() if (
                    "(" in key and ")" in key) or ("-" in key and "ID" not in key))

    return [Lookup_AnswerText(answerText, 0) for answerText in answerTexts]


def get_score_datas(reports):
    score_datas = []
    for report in reports:
        if report['data']:
            score_data_info = report['data'][0]
            score_data = ScoreData(0, report['report_id'], score_data_info['Enrollment'],
                                   score_data_info['Responses'], score_data_info['Declines'])
            score_datas.append(score_data)
    return score_datas


def get_questions_and_answers(reports, score_datas, question_texts, answer_texts):
    question_texts_lookup = {
        qt['text']: qt['questionTextID'] for qt in question_texts}
    answer_texts_lookup = {at['text']: at['answerTextID']
                           for at in answer_texts}
    score_datas_lookup = {sd['reportID']: sd['dataID'] for sd in score_datas}
    questions = []
    answers = []

    questionID = 1

    for report in reports:
        for raw_q in (report['data'][1:] if len(report['data']) > 1 else []):
            # print(raw_q)
            # find_first(question_texts, lambda qt: qt['text'] == raw_q.get("Question Text", None))
            qtext_id = question_texts_lookup.get(
                raw_q.get("Question Text", None), None)
            # find_first(score_datas, lambda sd: sd['reportID'] == report['report_id'])
            score_data_id = score_datas_lookup.get(report['report_id'], None)
            question = Question(questionID, raw_q.get('Question-ID', None), raw_q.get("Response Count", None),
                                raw_q.get("Response Rate", None),
                                raw_q.get(
                                    "Mean", None), raw_q.get("Median", None), raw_q.get("Std Dev", None),
                                qtext_id or qtext_id,
                                score_data_id or score_data_id)
            questions.append(question)

            for ans_text, val in raw_q.items():
                if ("(" in ans_text and ")" in ans_text) or ("-" in ans_text and "ID" not in ans_text):
                    ans_text_id = answer_texts_lookup.get(ans_text, None)
                    answer = Answer(0, ans_text_id, questionID, val)
                    answers.append(answer)
            questionID += 1

    return questions, answers


def get_departments(reports):
    def get_department(obj):
        return Department(0, obj['department_code'], obj['title'])

    return [get_department(report['department']) for report in reports]


def get_unique_departments(departments):
    return [Department(ind + 1, d['code'], d['title']) for ind, d in
            enumerate(make_unique_json(departments))]


def get_courses(reports, departments):
    def get_course(obj):
        def match_department(department):
            return department.code == obj['department']['department_code'] \
                   and department.title == obj['department']['title']

        return Course(obj['id'], obj['report_id'], obj['instructor']['instructorID'], obj['term']['termID'],
                      obj['name'], obj['subject'], obj['number'], obj['section'], obj['crn'],
                      find_first(departments, match_department).departmentID)

    return [get_course(report) for report in reports]


def get_terms(reports):
    def get_term(obj):
        return Term(obj['term']['termID'], obj['term']['title'])

    return [get_term(report) for report in reports]


def get_instructors(reports):
    def get_instructor(obj):
        return Instructor(obj['instructor']['instructorID'], obj['instructor']['firstName'],
                          obj['instructor']['middleName'], obj['instructor']['lastName'])

    return [get_instructor(report) for report in reports]


def get_all_comments(reports):
    all_comments = []

    def get_report_comments(report, comment_id):
        return [Comment(comment_id + ind, c, report['report_id']) for ind, c in enumerate(report['comments'])]
    _comment_id = 1
    for _report in reports:
        all_comments.extend(get_report_comments(_report, _comment_id))
        _comment_id = len(all_comments) + 1

    return all_comments


def write_files():
    reports = get_all_reports()

    departments = get_departments(reports)
    unique_departments = get_unique_departments(departments)

    courses = get_courses(reports, unique_departments)
    instructors = get_instructors(reports)
    terms = get_terms(reports)

    write_file(terms, "data/terms.csv")
    write_file(courses, "data/courses.csv")
    write_file(instructors, "data/instructors.csv")
    write_file(unique_departments, "data/departments.csv")

    comments = get_all_comments(reports)

    write_file(comments, "data/comments.csv")

    lookup_answertexts = get_lookup_answertexts(reports)
    lookup_questiontexts = get_lookup_questiontexts(reports)
    score_datas = get_score_datas(reports)

    unique_lookup_answertexts = make_unique_json(lookup_answertexts)
    unique_lookup_questiontexts = make_unique_json(lookup_questiontexts)
    unique_score_datas = make_unique_json(score_datas)

    write_file(lookup_answertexts, "data/answertexts.csv",
               unique_lookup_answertexts)
    write_file(lookup_questiontexts, "data/questiontexts.csv",
               unique_lookup_questiontexts)
    write_file(score_datas, "data/scoredatas.csv", unique_score_datas)

    questions, answers = get_questions_and_answers(
        reports, unique_score_datas, unique_lookup_questiontexts, unique_lookup_answertexts)

    write_file(questions, "data/questions.csv")
    write_file(answers, "data/answers.csv")


def write_file(obj_list, file_name, json_list=None):
    json_list = make_unique_json(obj_list) if json_list is None else json_list
    print(f'Saving {file_name}')
    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        csvwriter = csv.writer(f)

        count = 0

        for json_obj in json_list:
            if count == 0:
                header = json_obj.keys()
                csvwriter.writerow(header)
                count += 1

            csvwriter.writerow(json_obj.values())


if __name__ == "__main__":
    write_files()
