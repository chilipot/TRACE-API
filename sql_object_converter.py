import json
import csv
import requests
from collections import OrderedDict
import complex_json_encoder as cje
import numpy as np
  
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

class Course(cje.ComplexJSONSerializable):
	def __init__(self, id, instructorID, termID, name, subject, number, section, dataID):
		self.courseID = id
		self.instructorID = instructorID
		self.termID = termID
		self.name = name
		self.subject = subject
		self.number = number
		self.section = section
		self.dataID = dataID

def get_all_reports():
	reports = []
	for pageNumber in range(0, 106):
		url = 'https://trace-api.herokuapp.com/report?pageNumber=' + str(pageNumber) + '&pageSize=250'
		response = requests.get(url)
		results = json.loads(response.text)['result']
		reports += results
	
	return reports
	
def get_courses(reports):
	return [get_course(report) for report in reports]
	
def get_course(obj):
	return Course(obj['id'], obj['instructor']['instructorID'], obj['term']['termID'], obj['name'], obj['subject'], obj['number'], obj['section'], obj['_id']['$oid'])

def get_terms(reports):
	return [get_term(report) for report in reports]
	
def get_term(obj):
	return Term(obj['term']['termID'], obj['term']['title'])
	
def get_instructors(reports):
	return [get_instructor(report) for report in reports]
	
def get_instructor(obj):
	return Instructor(obj['instructor']['instructorID'], obj['instructor']['firstName'], obj['instructor']['middleName'], obj['instructor']['lastName'])

def write_files():
	reports = get_all_reports()
	
	courses = get_courses(reports)
	instructors = get_instructors(reports)
	terms = get_terms(reports)
	
	write_file(courses, "courses.csv")
	write_file(instructors, "instructors.csv")
	write_file(terms, "terms.csv")

def write_file(obj_list, file_name):
	json_list = json.loads(json.dumps(obj_list, cls=cje.ComplexEncoder))
	json_list = list(np.unique(np.array(json_list)))
	
	print("Before - " + file_name + " : " + str(len(obj_list)))
	print("After - " + file_name + " : " + str(len(json_list)))
	
	with open(file_name, 'wb') as f:
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