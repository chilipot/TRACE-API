from . import ComplexJSONSerializable

class Instructor(ComplexJSONSerializable):
    def __init__(self, instructorID, firstName, middleName, lastName):
        self.instructorID = instructorID
        self.firstName = firstName
        self.middleName = middleName
        self.lastName = lastName

class Term(ComplexJSONSerializable):
    def __init__(self, termID, title):
        self.termID = termID
        self.title = title

class Report(ComplexJSONSerializable):
    def __init__(self, id, instructor, term, name, subject, number, section, data):
        self.id = id
        self.instructor = instructor
        self.term = term
        self.name = name
        self.subject = subject
        self.number = number
        self.section = section
        self.data = data