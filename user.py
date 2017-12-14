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
import time
from encryption import AESCipher

#DB and server details
serv_addr = "localhost"
port = "27017"
full_serv_addr = "http://127.0.0.1:5000"
mongo_db_addr = "mongodb://" + serv_addr + ":" + port
mongo_client = pymongo.MongoClient(mongo_db_addr)
mongo_db = mongo_client.dfs

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
	regResponse = requests.post(full_serv_addr + "/register", data=json.dumps(body), headers=headers)
	authResponse = requests.post(full_serv_addr + "/authenticate", data=json.dumps(body), headers=headers)

#Upload
def upload():
	directory = os.path.dirname(os.path.realpath('__file__'))

	file_name = input("File name: ")
	filePath = os.path.join(directory, file_name)
	file_in = open(filePath)
	file_contents = file_in.read()

	dfs_file_name = cipher.encode_string(file_name).decode()
	dfs_file_contents = cipher.encode_string(file_contents).decode()

	body = {"file_name": dfs_file_name, "file_contents": dfs_file_contents}
	response = requests.post(full_serv_addr + "/file/upload", data=json.dumps(body), headers=headers)

def poll(file_name):
	body = {"file_name": file_name}
	response = requests.post(full_serv_addr + "/file/check", data=json.dumps(body), headers=headers)
	if response.json().get("response_code") == 423:
		return False
	else:
		return True

#Download
def download():
	file_name = input("File name: ") #Name on server
	file_name = cipher.encode_string(file_name).decode()

	body = {"file_name": file_name}
	response = requests.post(full_serv_addr + "/file/download", data=json.dumps(body), headers=headers)

	if response.json().get("response_code") == 404:
		print("ERR: file not found")
		return
	elif response.json().get("response_code") == 423:
		available = False
		while(not available):
			print("Waiting for lock to release...")
			available = poll(file_name)
			if(available):
				#when available, get file
				response = requests.post(full_serv_addr + "/file/download", data=json.dumps(body), headers=headers)
			time.sleep(5)

	new_file_name = input("Save as: ")
	file_contents = cipher.decode_string(response.json().get("file_contents").encode())
	print(file_contents)

	file = open(new_file_name, "wb")
	file.write(file_contents)
	file.close()


#Edit
def edit():
	file_name = input("File name: ") #Name on server
	file_name = cipher.encode_string(file_name).decode()

	body = {"file_name": file_name}
	response = requests.post(full_serv_addr + "/file/download", data=json.dumps(body), headers=headers)
	lock_response = requests.post(full_serv_addr + "/file/lock", data=json.dumps(body), headers=headers)

	if response.json().get("response_code") == 404:
		print("ERR: file not found")
		return
	elif response.json().get("response_code") == 423:
		available = False
		while(not available):
			print("Waiting for lock to release...")
			available = poll(file_name)
			if(available):
				response = requests.post(full_serv_addr + "/file/download", data=json.dumps(body), headers=headers)
				lock_response = requests.post(full_serv_addr + "/file/lock", data=json.dumps(body), headers=headers)
			time.sleep(5)

	file_contents = cipher.decode_string(response.json().get("file_contents").encode())

	file_contents_str = file_contents.decode()
	append_text = input("Text to append: ")

	full_contents = file_contents_str + append_text

	#Now replace contents on server
	dfs_file_contents = cipher.encode_string(full_contents).decode()

	unlock_response = requests.post(full_serv_addr + "/file/unlock", data=json.dumps(body), headers=headers)
	body = {"file_name": file_name, "file_contents": dfs_file_contents}
	response = requests.post(full_serv_addr + "/file/upload", data=json.dumps(body), headers=headers)

#List
def listAll():
	response = requests.get(full_serv_addr + "/file/list", headers=headers)
	print(response.json())

#Caching!
def addToCache():
	print("adding!")
	user = mongo_db.users.find_one(self)

def checkCheck(file_name, file_timestamp):
	print("checking!")

def getFromCache():
	print("getting!")

if __name__ == '__main__':
	registration()
	print('###Welcome###\n\nFunctions: \nUpload\nDownload\nEdit\n')
	while True:
		command = input("Command: ")
		
		if(command.lower() == 'upload'):
			upload()
		elif(command.lower() == 'download'):
			download()
		elif(command.lower() == 'edit'):
			edit()
		elif(command.lower() == 'list'):	#list all files on dfs
			listAll()
		elif(command.lower() == 'test'):
			addToCache()
		else:
			print("Unrecognized command, please try again.")