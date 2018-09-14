from flask import Flask, jsonify, request, abort
from flask_pymongo import PyMongo
import bson.json_util as json_util

app = Flask(__name__)

username = 'readonly'
password = 'readonly'

app.config['MONGO_DBNAME'] = 'trace'
app.config['MONGO_URI'] = 'mongodb+srv://' + username + ':' + password + '@trace-uabdw.mongodb.net/trace?retryWrites=true'

mongo = PyMongo(app)
db = mongo.db;

@app.route('/report', methods=['GET'])
def get_all_reports():
	report = db.reports
	#print(report)
	
	params = request.args.to_dict()
	
	if not (params.get('pageNumber') is None or params.get('pageNumber').isdigit()) or not (params.get('pageSize') is None or params.get('pageSize').isdigit()):
		return jsonify({'error': '400 - Bad Request - pageNumber and pageSize must be integers'}), 400
		
	if not (params.get('instructorID') is None or params.get('instructorID').isdigit()) or not (params.get('termID') is None or params.get('termID').isdigit()) or not (params.get('courseID') is None or params.get('courseID').isdigit()): 
		return jsonify({'error': '400 - Bad Request - instructorID, termID, and courseID must be integers'}), 400
	
	pageNumber = int(params.get('pageNumber', 0))
	pageSize = int(params.get('pageSize', 0))
	
	textQuery = params.get('search')
	
	
	instructorID = int(params.get('instructorID', -1))
	termID = int(params.get('termID', -1))
	courseID = int(params.get('courseID', -1))
	
	query = {}
	
	skipVal = 0 if pageNumber == 0 else ((pageNumber * pageSize) - 1)
	
	if (instructorID != -1):
		query['instructor.instructorID'] = instructorID
		
	if (termID != -1): 
		query['term.termID'] = termID
		
	if (courseID != -1):
		query['id'] = courseID
	
	print(skipVal)
	print(pageSize)
	
	if (textQuery is not None):
		query['$text'] = { '$search': textQuery}
		metadata = { 'score': { '$meta': "textScore"} }
		queryResult = report.find(query, metadata).sort([('score', {'$meta': 'textScore'})])
	else:
		queryResult = report.find(query)

	output = []
	for s in queryResult.skip(skipVal).limit(pageSize):
		s.pop('data') # Testing Only
		output.append(s);
	return json_util.dumps({'result' : output})

if __name__ == '__main__':
	app.run(debug=True)