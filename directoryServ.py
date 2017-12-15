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
from stringHelper import getFileName, getFileExtension, getFormattedFileName
import array
import requests
import json
import time

application_manager = Blueprint('application_manager',__name__)

serv_addr = "localhost"
port = "27017"
full_serv_addr = "http://127.0.0.1:5000"
mongo_db_addr = "mongodb://" + serv_addr + ":" + port
mongo_client = pymongo.MongoClient(mongo_db_addr)
mongo_db = mongo_client.dfs	#connect in to dfs db

aes_key = "94CA61A3CFC9BB7B8FF07C723917851A"
cipher = AESCipher(aes_key)

headers = {"Content-type": "application/json"}

@application_manager.route('/file/upload', methods=['POST'])
def upload():
	data_in = request.get_json(force=True)
	print("hitting upload")

	temp = data_in.get("file_name")
	file_name = cipher.decode_string(temp.encode()).decode()
	file_contents = cipher.decode_string(data_in.get("file_contents").encode().decode())

	#Find a free server
	server = mongo_db.servers.find_one({"server_name":  cipher.decode_string(data_in.get("server_name")).decode()})
	server_info = {"server_id": server.get("id"), "server_name": server.get("server_name"), "server_address": server.get("port")}

	#Store
	data = {"file_name": getFileName(file_name), "file_type": getFileExtension(file_name), "server": server_info, "locked": False, "last_modified": time.time()}

	#does it already exist on this server?
	file_existing = mongo_db.files.find_one({"file_name": getFileName(file_name), "file_type": getFileExtension(file_name), "server": server_info})

	if file_existing is not None:	
		#Exists? Is it locked (ie: don't overwrite)
		if file_existing.get("locked") is True:
			print("ba;;s")
			return jsonify({"response_code": 423})
		mongo_db.files.update_one({"file_name": getFileName(file_name), "file_type": getFileExtension(file_name), "server": server_info}, {"$set": data})
	else:
		mongo_db.files.insert(data) #into files db (ie: where the file contents are)

	server_data = {"file_name": file_name, "file_contents": file_contents}
	mongo_db.servers.update_one(server, {"$set": {getFormattedFileName(file_name): server_data}})

	return jsonify({"response_code": 200})

@application_manager.route('/file/download', methods=['POST'])
def download():
	data_in = request.get_json(force=True)
	print("hitting download")

	server_name=cipher.decode_string( data_in.get("server_name")).decode()
	server = mongo_db.servers.find_one({"server_name": server_name})
	server_info = {"server_id": server.get("id"), "server_name": server.get("server_name"), "server_address": server.get("port")}
	print(server_info)

	file_name = cipher.decode_string(data_in.get("file_name")).decode()

	file =  mongo_db.files.find_one({"file_name": getFileName(file_name), "file_type": getFileExtension(file_name), "server": server_info})
	if file is None:
		jsonify({"response_code": 404})

	#Find where file is
	file_requested = mongo_db.files.find_one({"file_name": getFileName(file_name), "file_type": getFileExtension(file_name), "server": server_info})
	if file_requested.get("locked") is True:
		return jsonify({"response_code": 423})

	#Grab contents
	print(server)
	file_out = server.get(getFormattedFileName(file_name))
	
	file_contents=cipher.encode_string(file_out.get("file_contents").decode()).decode()
	print(file_contents)

	file_timestamp = cipher.encode_string(str(file_requested.get("last_modified"))).decode()

	response = {"file_name": cipher.encode_string(file_name).decode(), "file_contents": file_contents, "last_modified": file_timestamp}
	return jsonify(response)

@application_manager.route('/file/list', methods=['GET'])
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