#Master diretory service
from flask import Flask
from flask import jsonify
from flask import request
import pymongo
import base64
from Crypto.Cipher import AES
from pprint import pprint
from flask import Blueprint
import requests
import json
import os
import sys
from encryption import AESCipher

application = Flask(__name__)

aes_key = "94CA61A3CFC9BB7B8FF07C723917851A"
cipher = AESCipher(aes_key)

server_key = "7596DE01913A20EC9069DBE508C5FEA3"

serv_addr = "localhost"
port = "27017"
full_serv_addr = "http://127.0.0.1:5000"
mongo_db_addr = "mongodb://" + serv_addr + ":" + port
mongo_client = pymongo.MongoClient(mongo_db_addr)
mongo_db = mongo_client.dfs	#connect in to dfs db
headers = {"Content-type": "application/json"}

#Register for use with master system
def register():
	data = {"server_key": cipher.encode_string(server_key).decode()}
	response = requests.post(full_serv_addr + "/register_server", data=json.dumps(data), headers=headers)

if __name__ == '__main__':
	register()
	application.run()