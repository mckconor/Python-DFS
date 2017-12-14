from flask import Flask
from flask import jsonify
from flask import request
import pymongo
import base64
from Crypto.Cipher import AES
from pprint import pprint

from directoryServ import application_manager
from authServ import application_auth
from lockServ import application_lock

application = Flask(__name__)
application.register_blueprint(application_manager)
application.register_blueprint(application_auth)
application.register_blueprint(application_lock)

serv_addr = "localhost"
port = "27017"
mongo_db_addr = "mongodb://" + serv_addr + ":" + port
mongo_client = pymongo.MongoClient(mongo_db_addr)
mongo_db = mongo_client.dfs

mongo_db.users.drop()
mongo_db.servers.drop()
mongo_db.directories.drop()
mongo_db.files.drop()
mongo_db.locks.drop()

if __name__ == '__main__':
	application.run()
