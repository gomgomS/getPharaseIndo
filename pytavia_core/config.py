import os
import sys

# from pytavia_stdlib import idgen

G_FLASK_SECRET=b'_5#y2L"F4Q8z\n\xec]/'

# This is the home path for the home of this project
G_HOME_PATH=os.getcwd()


G_STATIC_URL_PATH           = "/static"
G_UPLOAD_PATH               = G_HOME_PATH + G_STATIC_URL_PATH + "/upload"
G_STORAGE_PATH               = G_HOME_PATH + G_STATIC_URL_PATH + "/storage"
G_UPLOAD_URL_PATH           = G_STATIC_URL_PATH + "/upload"

pytavia_dispatchDB  = "pytavia_dispatchDB"
pytavia_dispatch    = "mongodb://127.0.0.1:27017/"

#DEVELOPMENT

#Database
mainDB = "mainDB"
mainDB_string = "mongodb://127.0.0.1:27017/" + mainDB

#Local Storage


#this is where we have all the databases we  want to connect to
G_DATABASE_CONNECT  = [
    {"dbname" : mainDB , "dbstring" : mainDB_string  },
]

# G_RANDOM_START = config_json["G_RANDOM_START"]
# G_RANDOM_END   = config_json["G_RANDOM_END"]

G_RECORD_ADD_MODIFIED_TIMESTAMP = True
G_RECORD_ADD_ARCHIVED_TIMESTAMP = True
