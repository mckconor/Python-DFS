#Locks files while editting
from flask import Flask
from flask import jsonify
from flask import request
from flask import Blueprint
import pymongo
import base64
from Crypto.Cipher import AES
from pprint import pprint
from encryption import AESCipher
from stringHelper import getFileName, getFileExtension, getFormattedFileName

application_lock = Blueprint('application_lock',__name__)

serv_addr = "localhost"
port = "27017"
mongo_db_addr = "mongodb://" + serv_addr + ":" + port
mongo_client = pymongo.MongoClient(mongo_db_addr)
mongo_db = mongo_client.dfs

aes_key = "94CA61A3CFC9BB7B8FF07C723917851A"
cipher = AESCipher(aes_key)

server_key = "7596DE01913A20EC9069DBE508C5FEA3"

@application_lock.route('/file/lock', methods=['POST'])
def lockFile():
	data_in = request.get_json(force=True)

	file_name = cipher.decode_string(data_in.get("file_name")).decode()

	file_existing = mongo_db.files.find_one({"file_name": getFileName(file_name), "file_type": getFileExtension(file_name)})
	mongo_db.files.update_one(file_existing, {"$set": {"locked": True}})

	return jsonify({"response_code": 200})


@application_lock.route('/file/unlock', methods=['POST'])
def unlockFile():
	data_in = request.get_json(force=True)

	file_name = cipher.decode_string(data_in.get("file_name")).decode()

	file_existing = mongo_db.files.find_one({"file_name": getFileName(file_name), "file_type": getFileExtension(file_name)})
	mongo_db.files.update_one(file_existing, {"$set": {"locked": False}})

	return jsonify({"response_code": 200})


@application_lock.route('/file/add_to_wait_queue', methods=['POST'])
def addToQueue():
	data_in = request.get_json(force=True)

	#File requested
	file_name = cipher.decode_string(data_in.get("file_name")).decode()
	#and where it is

	#Requester details
	user_addr = cipher.decode_string(data_in.get("user_addr")).decode()

	data = {"file_name": file_name, user_addr: user_addr}

	#File exist in table?
	file_existing = mongo_db.locks.find_one({"file_name": getFormattedFileName(file_name)})
	if file_existing is None:
		mongo_db.locks.insert(data)
	else:
		mongo_db.locks.update_one(file_existing, {"$set": data})