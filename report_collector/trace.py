'''
This module contains functionality to download report info
(not including any scores) and convert it to object lists
'''

import json
import time

import trace_driver
from JSONSerializable import ComplexEncoder
from JSONSerializable.Serializers import Instructor, Term, Report

from report_collector import jsonprep


# ---------------------------------------------------
#            Get Report Info (No Scores)
# ---------------------------------------------------

def report_info_data(driver, termID, count=26270):
    driver.set_page_load_timeout(7200)
    # Get All Reports For A Term (Use this Info to Search for Report Data)

    driver.get("https://www.applyweb.com/eval/new/reportbrowser/evaluatedCourses?excludeTA=false&page=1&rpp=" + str(count) + "&termId=" + str(termID))

    time.sleep(15)
    print("Links Loaded")
    el = driver.find_element_by_tag_name("pre")
    pre = el.text
    time.sleep(15)
    print("Found Element")
    data = json.loads(pre)['data']
    print("JSON loaded")
    time.sleep(15)

    return data

def get_report_noScores(obj):
    instructor = Instructor(obj['instructorId'], obj['instructorFirstName'], obj['instructorMiddleName'], obj['instructorLastName'])
    term = Term(obj['termId'], obj['termTitle'])
    report = Report(obj['id'], instructor, term, obj['name'], obj['subject'], obj['number'], obj['section'], {})
    return report

def get_reports_noScores(data):
    reports = list(map(get_report_noScores, data))
    return reports

# ---------------------------------------------------
#            Download Score Spreadsheets
# ---------------------------------------------------

def download_all_scores(driver, reports_noScores):
    print("Downloading...")
    for report in reports_noScores:
        link = "https://www.applyweb.com/eval/new/showreport/excel?r=2&c=" + str(report.id) + "&i=" + str(report.instructor.instructorID) + "&t=" + str(report.term.termID) + "&d=false"
        print(f"Getting... {link}")
        driver.get(link)
    time.sleep(5)
    print("Download Complete!")


# ---------------------------------------------------
#            Include Scores with Reports
# ---------------------------------------------------

def match_report_score(report, score):
    score_inst = score[0]['Instructor']
    score_course = score[0]['Course']
    score_term = score[0]['Term']

    #report_inst = " ".join(list(filter(None.__ne__, [report.instructor.firstName, report.instructor.middleName, report.instructor.lastName])))
    report_inst = " ".join([name for name in [report.instructor.firstName, report.instructor.lastName] if name and name.strip()])
    report_term = report.term.title
    report_course = report.subject + report.number + " " + report.section + " " + report.name

    return report_inst == score_inst and report_term == score_term and report_course == score_course

def include_score(report, scores):
    matches = [score for score in scores if match_report_score(report, score)]

    if (len(matches) > 0):
        matched_score = matches[0]
        report.data = matched_score[1:]
    return report

def include_scores(reports, scores):
    return [include_score(report, scores) for report in reports]

# ---------------------------------------------------
#            Get Complete Report Objects
# ---------------------------------------------------

def get_all_reports():
    driver = trace_driver.auth()
    print("Getting Links")
    # data = report_info_data(driver, 0)

    with open('../data/reports_noScores (ALL).json') as f:
        data = json.load(f)['data']
    
    print("No_Scores")
    reports_noScores = get_reports_noScores(data)
    # download_all_scores(driver, reports_noScores)
    scores = jsonprep.get_all_scores()
    reports = include_scores(reports_noScores, scores)
    j = json.dumps(reports, cls=ComplexEncoder)
    with open('full_data.json', 'w') as f:
        f.write(j)

    print("Done")
    return reports

if __name__ == "__main__":
    get_all_reports()
