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

application_lock = Blueprint('application_lock',__name__)

serv_addr = "localhost"
port = "27017"
mongo_db_addr = "mongodb://" + serv_addr + ":" + port
mongo_client = pymongo.MongoClient(mongo_db_addr)
mongo_db = mongo_client.dfs

aes_key = "94CA61A3CFC9BB7B8FF07C723917851A"
cipher = AESCipher(aes_key)

server_key = "7596DE01913A20EC9069DBE508C5FEA3"