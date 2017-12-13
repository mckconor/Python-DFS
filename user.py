#Creates User
from flask import Flask
from flask import jsonify
from flask import request
import pymongo
import base64
from pprint import pprint
import requests
import json
import os
from encryption import AESCipher

#DB and server details
serv_addr = "localhost"
port = "27017"
full_serv_addr = "http://127.0.0.1:5000"
mongo_db_addr = "mongodb://" + serv_addr + ":" + port
mongo_client = pymongo.MongoClient(mongo_db_addr)
mongo_db = mongo_client.authServ	#connect in to auth db

#User details
username = "test"
password = "password1"
public_key = "PUBLICKEY"

# file_name = "test.txt"

aes_key = "94CA61A3CFC9BB7B8FF07C723917851A"
cipher = AESCipher(aes_key)

headers = {"Content-type": "application/json"}

#create and authenticate users
#return and allow custom user name and restrict dupes
def registration():
	body = {"username": username, "password": str(cipher.encode_string(password), 'utf-8'), "public_key": public_key}
	requests.post(full_serv_addr + "/register", data=json.dumps(body), headers=headers)
	requests.post(full_serv_addr + "/authenticate", data=json.dumps(body), headers=headers) 

#Upload
def upload():
	directory = os.path.dirname(os.path.realpath('__file__'))

	file_name = input("File name: ") #Where on the file system, blank for root
	filePath = os.path.join(directory, file_name)
	file_in = open(filePath)
	file_contents = file_in.read()

	dfs_file_name = str(cipher.encode_string(file_name))
	dfs_file_contents = str(cipher.encode_string(file_contents))

	body = {"file_name": dfs_file_name, "file_contents": dfs_file_contents}
	response = requests.post(full_serv_addr + "/file/upload", data=json.dumps(body), headers=headers)


if __name__ == '__main__':
	registration()
	print('###Welcome###\n\nFunctions: \nUpload\nDownload\nEdit\n')
	while True:
		command = input("Command: ")
		
		if(command == 'Upload'):
			upload()
		elif(command == 'Download'):
			download()
		else:
			edit()