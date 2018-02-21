from src import app
from flask import jsonify, json
from flask import Flask,render_template,make_response
from flask import request
import requests

@app.route("/")
def home():
    return "Hasura Hello World"

@app.route("/hello")
def hello_world():
	return "Hello World - Thiru"
# Uncomment to add a new URL at /new

@app.route("/form",methods=['POST'])
def form():
	if request.method == 'POST': #this block is only entered when the form is submitted
		metric = request.form.get('metric')
		return '''<h1>The metric value is: {}</h1>'''.format(metric)

	return '''<form method="POST">
            Metric: <input type="text" name="metric"><br>
            <input type="submit" value="Submit"><br>
            </form>'''
	
@app.route("/getmetric",methods=['POST'])
def get_metric():
	#get the metric from front-end
	jsonMetric = request.get_json()
	
	#converting to json object
	jsonData = json.loads(jsonMetric)
	
	metric = jsonData['metric']

	# This is the url to which the query is made
	url = "https://data.declassification29.hasura-app.io/v1/query"

	# This is the json payload for the query
	requestPayload = {
		"type": "select",
		"args": {
			"table": "world_happiness_report",
			"columns": [
				"*"
			],
			"order_by": [
				{
					"column": "ID"
				}
			]
		}
	}

	# Setting headers
	headers = {
		"Content-Type": "application/json"
	}

	# Make the query and store response in resp
	dbresp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
	
	#converting the response to json object
	respjson = json.loads(dbresp.content)
	
	result = {}	
	i = 0
	#looping through the list object
	for index, value in enumerate(respjson):
		#looping through the dict  using dict comprehension
		temp = {x:y for x,y in value.items() if x in ('Country',metric)}
		result[i] = {}
		result[i] = temp
		i += 1
	
	anslist = json.dumps(result)
	
	return anslist