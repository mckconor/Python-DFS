#Master diretory service
from flask import Flask
from flask import jsonify
from flask import request
import pymongo
import base64
from Crypto.Cipher import AES
from pprint import pprint
from flask import Blueprint
from encryption import AESCipher
import array

application_master = Blueprint('application_master',__name__)

serv_addr = "localhost"
port = "27017"
mongo_db_addr = "mongodb://" + serv_addr + ":" + port
mongo_client = pymongo.MongoClient(mongo_db_addr)
mongo_db = mongo_client.dfs	#connect in to dfs db

aes_key = "94CA61A3CFC9BB7B8FF07C723917851A"
cipher = AESCipher(aes_key)

def getFileName(string):
	return string.split(".")[0]

def getFileExtension(string):
	return string.split(".")[1]

def getFormattedFileName(string):
	return getFileName(string) + "\u2024" + getFileExtension(string)

@application_master.route('/file/upload', methods=['POST'])
def upload():
	data_in = request.get_json(force=True)
	print("hitting upload")

	temp = data_in.get("file_name")
	file_name = cipher.decode_string(temp.encode()).decode()
	file_contents = cipher.decode_string(data_in.get("file_contents").encode().decode())

	#Find a free server
	server = mongo_db.servers.find_one()
	server_info = {"server_id": server.get("id"), "server_address": server.get("port")}

	#Store
	data = {"file_name": getFileName(file_name), "file_type": getFileExtension(file_name), "server": server_info, "locked": False}

	#does it already exist on this server?
	file_existing = mongo_db.files.find_one({"file_name": getFileName(file_name), "file_type": getFileExtension(file_name)})
	if file_existing is not None:
		mongo_db.files.update_one({"file_name": getFileName(file_name), "file_type": getFileExtension(file_name)}, {"$set": data})
	else:
		mongo_db.files.insert(data) #into files db (ie: where the file contents are)

	server_data = {"file_name": file_name, "file_contents": file_contents}
	mongo_db.servers.update_one(server, {"$set": {getFormattedFileName(file_name): server_data}})

	return jsonify({"response_code": 200})

@application_master.route('/file/download', methods=['POST'])
def download():
	data_in = request.get_json(force=True)
	print("hitting download")

	file_name = cipher.decode_string(data_in.get("file_name")).decode()

	#Find where file is
	server = mongo_db.files.find_one({"file_name": getFileName(file_name), "file_type": getFileExtension(file_name)}).get("server")
	if server is None:
		return jsonify({"response_code": 404})

	#Grab them contents boii
	print(server)
	file_out = mongo_db.servers.find_one({"id": server.get("server_id")}).get(getFormattedFileName(file_name))
	
	file_contents=cipher.encode_string(file_out.get("file_contents").decode()).decode()
	print(file_contents)

	response = {"file_name": cipher.encode_string(file_name).decode(), "file_contents": file_contents}
	return jsonify(response)

@application_master.route('/file/list', methods=['GET'])
def listAll():
	all_files = mongo_db.files.find()

	jsonString = {}
	if(all_files.count() <= 0):
		return jsonify({"response_code": 403})
	for i in range(all_files.count()):
		file_name = all_files[i].get("file_name")
		file_status = all_files[i].get("status")
		file_server = all_files[i].get("server").get("id")
		jsonString.update({"file_name": file_name, "lock_status": file_status, "server": file_server})

	return jsonify(jsonString)

# if __name__ == '__main__':
	# application.run()