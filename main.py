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

if __name__ == '__main__':
	application.run()
