'''
This module contains functionality to download report info
(not including any scores) and convert it to object lists
'''

import json
import time

from bs4 import BeautifulSoup

import trace.pipeline.authentication as auth
import trace.pipeline.complex_json_encoder as cje
import trace.pipeline.jsonprep as jsonprep


# ---------------------------------------------------
#            Report Metadata Data Model
# ---------------------------------------------------
class Instructor(cje.ComplexJSONSerializable):
    def __init__(self, instructorID, firstName, middleName, lastName):
        self.instructorID = instructorID
        self.firstName = firstName
        self.middleName = middleName
        self.lastName = lastName


class Term(cje.ComplexJSONSerializable):
    def __init__(self, termID, title):
        self.termID = termID
        self.title = title


class Department(cje.ComplexJSONSerializable):
    def __init__(self, departmentID, department_code, title):
        self.departmentID = departmentID
        self.department_code = department_code
        self.title = title


class Report(cje.ComplexJSONSerializable):
    def __init__(self, id, instructor, term, name, subject, number, section, data, crn, department, comments=[]):
        self.id = id
        if isinstance(instructor, dict):
            self.instructor = Instructor(**instructor)
        else:
            self.instructor = instructor
        if isinstance(term, dict):
            self.term = Term(**term)
        else:
            self.term = term
        if isinstance(department, dict):
            self.department = Department(**department)
        else:
            self.department = department
        self.name = name
        self.subject = subject
        self.number = number
        self.section = section
        self.crn = crn
        self.data = data
        self.comments = comments
        self.department = department


# ---------------------------------------------------
#            Get Report Info (No Scores)
# ---------------------------------------------------
def report_info_data(driver, termID, count=100000):
    driver.set_page_load_timeout(7200)
    # Get All Reports For A Term (Use this Info to Search for Report Data)

    driver.get("https://www.applyweb.com/eval/new/reportbrowser/evaluatedCourses?excludeTA=false&page=1&rpp=" + str(
        count) + "&termId=" + str(termID))

    print("Links Loaded")
    el = driver.find_element_by_tag_name("pre")
    pre = el.text
    print("Found Element")
    data = json.loads(pre)['data']
    print("JSON loaded")

    return data


def get_reports_noScores(data):
    def get_report_noScores(obj):
        instructor = Instructor(obj['instructorId'], obj['instructorFirstName'], obj['instructorMiddleName'],
                                obj['instructorLastName'])
        term = Term(obj['termId'], obj['termTitle'])
        department = Department(0, obj['departmentCode'], obj['departmentName'])
        report = Report(obj['id'], instructor, term, obj['name'], obj['subject'], obj['number'], obj['section'], {},
                        obj['sourceId'], department)
        return report

    reports = [get_report_noScores(r) for r in data]
    return reports


# ---------------------------------------------------
#            Retrieve Report Comments
# ---------------------------------------------------

def scrape_comments(driver, reports_noScores):
    driver.set_page_load_timeout(100000)
    seen_terms = set()
    for report in reports_noScores:
        url = f'https://www.applyweb.com/eval/new/showreport?c={report.id}&i={report.instructor.instructorID}&t={report.term.termID}&r=9&d=true'
        driver.get(url)
        time.sleep(1)
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'lxml')
        a_tags = soup.find_all(lambda tag: tag.name == 'a' and tag.parent and tag.parent.name == 'td')
        comments = [a.text.strip() for a in a_tags]
        report.comments = comments
        if report.term.termID not in seen_terms:
            seen_terms.add(report.term.termID)
            print(f"Scraped comments for term {report.term.termID}")
    return reports_noScores


# ---------------------------------------------------
#            Download Score Spreadsheets
# ---------------------------------------------------

def download_all_scores(driver, reports_noScores):
    print("Downloading...")
    for report in reports_noScores:
        driver.get("https://www.applyweb.com/eval/new/showreport/excel?r=2&c=" + str(report.id) + "&i=" + str(
            report.instructor.instructorID) + "&t=" + str(report.term.termID) + "&d=false")
    time.sleep(5)
    print("Download Complete!")


# ---------------------------------------------------
#            Include Scores with Reports
# ---------------------------------------------------

def include_scores(reports, _scores):
    def include_score(report, scores):
        report_inst = " ".join(
            [name for name in [report.instructor.firstName, report.instructor.lastName] if name and name.strip()])
        report_term = report.term.title
        report_course = report.subject + report.number + " " + report.section + " " + report.name

        def match_score(score):
            return report_inst == score[0]['Instructor'] and report_term == score[0]['Term'] and report_course == \
                   score[0][
                       'Course']

        matches = [score for score in filter(match_score, scores)]

        if len(matches) > 0:
            print("***MATCHED***")
            matched_score = matches[0]
            report.data = matched_score[1:]
        return report

    for ind, _report in enumerate(reports):
        print("Finished Report #%d" % ind)
        yield include_score(_report, _scores)


# ---------------------------------------------------
#            Get Complete Report Objects
# ---------------------------------------------------

def get_all_reports():
    driver = auth.auth()
    print("Getting Links")

    term_list = reversed([75, 82, 83, 84, 87])

    all_reports_no_scores = []
    for term in term_list:
        # data = report_info_data(driver, term)
        #
        # reports_noScores = get_reports_noScores(data)
        #
        # j = json.dumps(reports_noScores, cls=cje.ComplexEncoder)
        # with open(f'data/reports_noScores-term-{term}.json', 'w') as f:
        #     f.write(j)

        with open(f'data/reports_noScores-term-{term}.json', 'r') as f:
            reports_noScores = [Report(**r) for r in json.load(f)]

        all_reports_no_scores.extend(reports_noScores)

    print("Got Reports No_Scores")

    all_reports_with_comments = scrape_comments(driver, all_reports_no_scores)

    j = json.dumps(all_reports_with_comments, cls=cje.ComplexEncoder)
    with open(f'data/reports_no_scores_with_comments.json', 'w') as f:
        f.write(j)

    print("Saved Reports No Scores With Comments")

    download_all_scores(driver, all_reports_no_scores)
    scores = jsonprep.get_all_scores()
    with open('data/all_scores.json', 'w') as f:
        json.dump(scores, f)

    print("Got Scores")

    reports = list(include_scores(all_reports_with_comments, scores))
    print("Matched Reports and Scores")

    j = json.dumps(reports, cls=cje.ComplexEncoder)
    with open('data/full_data.json', 'w') as f:
        f.write(j)

    print("Wrote File")

    return reports


if __name__ == "__main__":
    get_all_reports()
    print("Done")
