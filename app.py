from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo, ObjectId
from pymongo import cursor
import bson.json_util as json_util
import time

app = Flask(__name__)
cors = CORS(app)

username = 'readonly'
password = 'readonly'

app.config['MONGO_DBNAME'] = 'trace'
app.config['MONGO_URI'] = 'mongodb+srv://' + username + ':' + password + '@trace-uabdw.mongodb.net/trace?retryWrites=true'
app.config['CORS_HEADERS'] = 'Content-Type'

mongo = PyMongo(app)
db = mongo.db;

@app.route('/report', methods=['GET'])
@cross_origin()
def get_all_reports():
	start = time.time()
	report = db.reports
	#print(report)
	
	params = request.args.to_dict()
	
	if not params:
		return jsonify({'error': '400 - Bad Request - pageNumber and pageSize are both missing'}), 400
	
	if not (params.get('pageNumber') is None or params.get('pageNumber').isdigit()) or not (params.get('pageSize') is None or params.get('pageSize').isdigit()):
		return jsonify({'error': '400 - Bad Request - pageNumber and pageSize must be integers'}), 400
	
	if not (params.get('pageSize') is None or (params.get('pageSize').isdigit() and int(params.get('pageSize')) <= 250)):
		return jsonify({'error': '400 - Bad Request - pageSize is capped at 250'}), 400
	
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
	
	#print(skipVal)
	#print(pageSize)
	
	if (textQuery is not None):
		query['$text'] = { '$search': textQuery}
		metadata = { 'score': { '$meta': "textScore"} , 'data' : 0}
		end1 = time.time()
		queryPointer = report.find(query, metadata).sort([('score', {'$meta': 'textScore'})])
		end2 = time.time();
	else:
		end1 = time.time()
		queryPointer = report.find(query, {'data' : 0})
		queryPointer.batch_size(1000000)
		queryPointer.cursor_type = cursor.CursorType.EXHAUST
		end2 = time.time()

	output = []
	queryResult = queryPointer.skip(skipVal).limit(pageSize)
	end3 = time.time()
	'''
	for s in queryResult:
		#s.pop('data') # Testing Only
		output.append(s);
	'''
	output = list(queryResult)
	end4 = time.time()
	
	print("Up to query: " + str(end1 - start))
	print("Query: " + str(end2 - end1))
	print("Load from pointer: " + str(end3 - end2))
	print("Iteration: " + str(end4 - end3))
	
	return json_util.dumps({'result' : output})

@app.route('/report/<objectID>', methods=['GET'])
@cross_origin()
def get_single_report(objectID):
	params = request.args.to_dict()
	just_score = params.get('justScore', False)
	
	if just_score.lower() == 'true':
		result = db.reports.find_one({'_id' : ObjectId(objectID)}, {'_id' : 1, 'data' : 1})
	else:
		result = db.reports.find_one({'_id' : ObjectId(objectID)})
		
	return json_util.dumps({'result': result})
	
if __name__ == '__main__':
	app.run(debug=True)