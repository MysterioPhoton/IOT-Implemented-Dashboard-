from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from datetime import datetime
from itsdangerous import json

import requests
from script import addToFirestore, getFromFirestore

def get_current_time():
	now = datetime.now()
	current_time = now.strftime("%D %H:%M:%S")
	return current_time

app = Flask(__name__)
api = Api(app)

data_put_args = reqparse.RequestParser()
data_put_args.add_argument("temperature", type=float, help="temperature not provided", required=True)

class Data(Resource):
	def get(self):
		return {'data': getFromFirestore()}
	def put(self):
		temperature = data_put_args.parse_args().temperature
		addToFirestore(temperature, get_current_time())
		return {"message": "temperature added successfully"}, 201

def getDeviceState():
	res = requests.get("http://192.168.0.241")
	return json.loads(res.text)['state']

status_patch_args = reqparse.RequestParser()
status_patch_args.add_argument("state", type=str, help="state not provided", required=True)

def abort_if_invalid_desired_state(desired_state):
	if (desired_state != "on") and (desired_state != "off"):
		abort(401, message="invalid state requested")

class Status(Resource):
	def get(self, desired_state):
		abort_if_invalid_desired_state(desired_state)
		requests.get("http://192.168.0.241/{}".format(desired_state))
		return {"state": getDeviceState()}
	# def post(self):
	# 	desired_state = status_patch_args.parse_args().state
	# 	abort_if_invalid_desired_state(desired_state)
	# 	requests.get("http://192.168.0.241/{}".format(desired_state))
	# 	return {"state": getDeviceState()}, 201

api.add_resource(Data, "/data")
api.add_resource(Status, "/status/<string:desired_state>")

@app.after_request
def after_request(response):
	response.access_control_allow_origin = "*"
	return response

if __name__ == "__main__":
	app.run(host="0.0.0.0",debug=True)