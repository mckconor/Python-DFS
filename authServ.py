#Verifies user
from flask import Flask
from flask import jsonify
from flask import request
from flask import Blueprint
import pymongo
import base64
from Crypto.Cipher import AES
from pprint import pprint

application_auth = Blueprint('application_auth',__name__)

serv_addr = "localhost"
port = "27017"
mongo_db_addr = "mongodb://" + serv_addr + ":" + port
mongo_client = pymongo.MongoClient(mongo_db_addr)
mongo_db = mongo_client.dfs

aes_key = "94CA61A3CFC9BB7B8FF07C723917851A"
server_key = "7596DE01913A20EC9069DBE508C5FEA3"

mongo_db.users.drop()
mongo_db.servers.drop()
mongo_db.directories.drop()
mongo_db.files.drop()

# def encode_string(key, string):
# 	encoded = []
# 	for i in range(len(string)):
# 		key_char = key[i % len(key)]
# 		encoded_char = chr(ord(string[i]) + ord(key_char) % 256)
# 		encoded.append(encoded_char)
# 	encoded_string = "".join(encoded)
# 	return base64.urlsafe_b64encode(AES.new(key, AES.MODE_ECB).encrypt(encoded_string))

def encode_string(key, string):
	ba = bytearray()
	ba.extend(map(ord, string))
	length = 16 - (len(string) % 16)
	ba += bytes([length]) * length
	return base64.urlsafe_b64encode(ba)

def decode_string(key, string):
    string = base64.urlsafe_b64decode(string)
    string = string[:-string[-1]]
    return string.decode('utf-8')

@application_auth.route('/test', methods=['GET', 'POST'])
def test():
	print("test post")
	return jsonify({})

@application_auth.route('/register', methods=['POST'])
def register():
	user_data = request.get_json(force=True)

	user_username = user_data.get('username')
	user_password = user_data.get('password')
	public_key = user_data.get('public_key')

	# user_password = encode_string(aes_key, user_password)

	# if(mongo_db.users.find_one({'username': in_username})) == True:
	# 	#User already exists
	# 	jsonString = {"response_code": 500}
	# 	return jsonify(jsonString)
	
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