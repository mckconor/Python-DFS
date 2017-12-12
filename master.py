#Master diretory service
from flask import Flask
from flask import jsonify
from flask import request
import pymongo
import base64
from Crypto.Cipher import AES
from pprint import pprint
from flask import Blueprint
from encryption import encode_string, decode_string

application_master = Blueprint('application_master',__name__)

serv_addr = "localhost"
port = "27017"
mongo_db_addr = "mongodb://" + serv_addr + ":" + port
mongo_client = pymongo.MongoClient(mongo_db_addr)
mongo_db = mongo_client.dfs	#connect in to dfs db

@application_master.route('/file/upload', methods=['POST'])
def upload():
	data_in = request.get_data()
	print("hitting upload")

	file_name = decode_string(data_in.get("file_name"))
	file_contents = decode_string(data_in.get("file_contents"))

	#Find a free server
	server = mongo_db.servers.findOne()

	#Store that bad boy
	data = {"file_name": file_name, "server": server}
	mongo_db.files.insert(data) #into files db (ie: where the file contents are)
	mongo_db.servers.update_one(server, {"$set": {"file": data_in}}) #"file_name": file_name, "file_contents": file_contents}

	return jsonify({"response_code": 200})

@application_master.route('/file/download', methods=['POST'])
def download():
	data_in = request.get_data()
	print("hitting download")

	file_name = decode_string(data_in.get("file_name"))

	#Find where file is
	server = mongo_db.files.findOne({"file_name": file_name})

	#Grab them contents boii
	file = mongo_db.servers.findOne(server).get("file")

	print(file)
	return jsonify({"response_code": 200})


# if __name__ == '__main__':
	# application.run()