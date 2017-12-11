from flask import Flask
from flask import jsonify
from flask import request
import pymongo
import base64
from Crypto.Cipher import AES
from pprint import pprint

from master import application_master
from authServ import application_auth

application = Flask(__name__)
application.register_blueprint(application_master)
application.register_blueprint(application_auth)

serv_addr = "localhost"
port = "27017"
mongo_db_addr = "mongodb://" + serv_addr + ":" + port
mongo_client = pymongo.MongoClient(mongo_db_addr)
mongo_db = mongo_client.dfs

mongo_db.users.drop()
mongo_db.servers.drop()
mongo_db.directories.drop()
mongo_db.files.drop()

if __name__ == '__main__':
	application.run()
