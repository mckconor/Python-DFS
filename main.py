from flask import Flask
import pymongo

mongo_server = "localhost"
mongo_port = "27017"
connect_string = "mongodb://" + mongo_server + ":" + mongo_port
connection = pymongo.MongoClient(connect_string)

db = connection.project

db.servers.insert(
		{"id": 1}
	)
