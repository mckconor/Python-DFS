#Verifies user
from flask import Flask
from flask import jsonify
from flask import request
from flask import Blueprint
import pymongo
import base64
from Crypto.Cipher import AES
from pprint import pprint
from encryption import encode_string, decode_string

application_auth = Blueprint('application_auth',__name__)

serv_addr = "localhost"
port = "27017"
mongo_db_addr = "mongodb://" + serv_addr + ":" + port
mongo_client = pymongo.MongoClient(mongo_db_addr)
mongo_db = mongo_client.dfs

aes_key = "94CA61A3CFC9BB7B8FF07C723917851A"
server_key = "7596DE01913A20EC9069DBE508C5FEA3"


@application_auth.route('/test', methods=['GET', 'POST'])
def test():
	print("test post")
	return jsonify({})

##
#Registers individ servers
##
@application_auth.route('/register_server', methods=['POST'])
def register_server():
	server_data = request.get_json(force=True)

	#very basic server auth
	if server_data.get('server_key') != str(encode_string(aes_key, server_key)):
		print("serv key in: ", server_data.get('server_key'))
		print("serv key here: ", encode_string(aes_key, server_key))
		jsonString = {"response_code": 403} #forbidden
		return jsonify(jsonString)

	server_id = get_new_server_details()
	server_addr = request.remote_addr
	
	server = {"id": server_id,"address": server_addr}
	mongo_db.servers.insert(server)

	jsonString = {"response_code": 200}
	return jsonify(jsonString)

def get_new_server_details():
	server_id = mongo_db.servers.count()
	return server_id

##
#Registers users
##
@application_auth.route('/register', methods=['POST'])
def register():
	user_data = request.get_json(force=True)

	user_username = user_data.get('username')
	user_password = user_data.get('password')
	public_key = user_data.get('public_key')
	
	user = {"id": mongo_db.users.count()+1,"username": user_username, "password": user_password, "public_key": public_key, "server_key": ""}
	mongo_db.users.insert(user)

	print(user)

	jsonString = {"response_code": 200}
	return jsonify(jsonString)

@application_auth.route('/authenticate', methods=['POST'])
def authenticate():
	in_data = request.get_json(force=True)

	in_username = in_data.get('username')
	in_password = in_data.get('password')

	current_user = mongo_db.users.find_one({'username': in_username})
	# encoded_pass = encode_string(aes_key, in_password)

	jsonString = {}
	if(in_password == current_user['password']):
		current_user['server_key'] = "9F9F78CA3F46944FF10CDAD5C8584356"
		mongo_db.users.update_one({'username': in_username}, {"$set": current_user}, upsert=False)
		users = mongo_db.users.find({})
		for x in users:
			pprint(x)
		jsonString = {"response_code": 200}
	else:
		jsonString = {"response_code": 404}

	return jsonify(jsonString)

@application_auth.route('/logout', methods=['POST'])
def logout():
	in_data = request.get_json(force=True)

	in_username = in_data.get('username')
	current_user = mongo_db.users.find_one({'username': in_username})
	current_user['session_id'] = ""
	mongo_db.users.update_one({'username': in_username}, {"$set": current_user}, upsert=False)
	users = mongo_db.users.find({})
	for x in users:
		pprint(x)

	jsonString = {"response_code": 200}
	return jsonify(jsonString)

# if __name__ == '__main__':
# 	application.run()