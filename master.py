#Master diretory service
from flask import Flask
from flask import jsonify
from flask import request
import pymongo
import base64
from Crypto.Cipher import AES
from pprint import pprint
from flask import Blueprint

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
	return jsonify({"succ": True})


# if __name__ == '__main__':
# 	with application.app_context():
# 		application.run()