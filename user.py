#Creates User
from flask import Flask
from flask import jsonify
from flask import request
import pymongo
import base64
from Crypto.Cipher import AES
from pprint import pprint
import requests
import json
import os

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

file_name = "test.txt"

aes_key = "94CA61A3CFC9BB7B8FF07C723917851A"

headers = {"Content-type": "application/json"}

def encode_string(key, string):
	ba = bytearray()
	ba.extend(map(ord, string))
	length = 16 - (len(string) % 16)
	ba += bytes([length]) * length
	return base64.urlsafe_b64encode(ba)

def decode_string(key, string):
    string = base64.urlsafe_b64decode(string)
    string = string[:-string[-1]]
    return string.decode("utf-8")

#create and authenticate users
for i in range(2):
	body = {"username": username + str(i), "password": str(encode_string(aes_key, password), 'utf-8'), "public_key": public_key}
	requests.post(full_serv_addr + "/register", data=json.dumps(body), headers=headers)
	requests.post(full_serv_addr + "/authenticate", data=json.dumps(body), headers=headers) 

#Upload
def upload():
	directory = os.path.dirname(os.path.realpath('__file__'))
	filePath = os.path.join(directory, file_name)
	file_in = open(filePath)
	file_contents = file_in.read()

	dfs_directory_location = encode_string(aes_key, input("Directory: ")) #Where on the file system, blank for root
	dfs_file_name = encode_string(aes_key, file_name)
	dfs_file_contents = encode_string(aes_key, file_contents)

	body = {"directory_location": dfs_directory_location.decode("utf-8"), "file_name": dfs_file_name.decode("utf-8"), "file_contents": dfs_file_contents.decode("utf-8")}
	uploaded_file = requests.post(full_serv_addr + "/file/upload", data=json.dumps(body), headers=headers)


if __name__ == '__main__':
	print('###Welcome###\n\nFunctions: \nUpload\nDownload\nEdit\n')
	while True:
		command = input("Command: ")
		
		if(command == 'Upload'):
			upload()
		elif(command == 'Download'):
			download()
		else:
			edit()