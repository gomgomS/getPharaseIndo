import json
import time
import pymongo
import sys
import urllib.parse
import base64
import traceback
import random
import urllib.request
import io
import requests
import json
import hashlib
import bcrypt

sys.path.append("pytavia_core")
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib")
sys.path.append("pytavia_storage")
sys.path.append("pytavia_modules")
sys.path.append("pytavia_modules")


from flask             import render_template_string
from flask             import render_template
from flask             import request
from flask             import session

from pytavia_stdlib    import idgen
from pytavia_stdlib    import utils
from pytavia_core      import database
from pytavia_core      import config
from pytavia_core      import helper
from pytavia_core      import bulk_db_insert
from pytavia_core      import bulk_db_update
from pytavia_core      import bulk_db_multi

from datetime          import datetime

from apscheduler.schedulers.background import BackgroundScheduler

class login_app:    
    mgdDB = database.get_db_conn(config.mainDB)   
    # sched = BackgroundScheduler()  
    # sched.start()       

    def __init__(self, app):
        self.webapp = app        
    # end def

    def process(self, params):        
        response = helper.response_msg(
            "CREATE_COMPANY_SUCCESS",
            "CREATE COMPANY SUCCESS", {},
            "0000"
        )
        
        data = params
 
        
        #start check existing user in db
        login_user    = self.mgdDB.db_users.find_one(
            {
                "status": {"$not":{"$regex":"DEACTIVE"}},
                "$or"   :[{
                        "name"  : data['emailorusername']
                    },
                    {
                        "email" : data['emailorusername']
                    }
                ]
            }
        )

        #check token active or not
        data_status_token_all = []
        token_data_get     = self.mgdDB.db_token_access.find(
            {
                "user_id": login_user['pkey']
                # "status_content": 'expired'
            },{"_id":0}
        ) 
        for temp_data in token_data_get:
            data_status_token_all.append(temp_data['status_token'])
        
        if 'active' in data_status_token_all:
            token_status = 'active'
        else:
            token_status = 'deactive'
       
        if login_user is not None:         
            self.webapp.logger.debug(login_user)     
            self.webapp.logger.debug("--------------true------------")        
            if bcrypt.hashpw(data['pass'].encode('utf-8'),login_user['password']) == login_user['password']:
                
                session['username'] = login_user['name']
                session['email']    = login_user['email']
                session['role']     = login_user['role'] 
                session['pkey']     = login_user['pkey'] 
                # session['token_status'] = token_status

                if session['role'] == 'admin':
                    response = {
                        'kboom' : 'UPLOAD_RAW'            
                    } 
                else:
                    response = 'dashboard'
            else:                                              
                response = {
                    "kboom" : "none",
                    "message_error":"Invalid username or email/password combination!!",
                    "number":"1"
                }
        else:            
            response = {
                    "kboom" : "none",
                    "message_error":"Invalid username",
                    "number":"2"
                }                              

        return response
    # end def

    def process_by_token(self, params):        
        response = helper.response_msg(
            "CREATE_COMPANY_SUCCESS",
            "CREATE COMPANY SUCCESS", {},
            "0000"
        )
        login_user = None
        data = params
        self.webapp.logger.debug(data)
        #start check existing user in db
       
        token_data_get     = self.mgdDB.db_token_access.find_one(
            {
                "token": data['token']
                # "status_content": 'expired'
            },{"_id":0}
        ) 
        self.webapp.logger.debug(token_data_get)

        if token_data_get is not None:
            if token_data_get['status_token'] == 'active':
                login_user    = self.mgdDB.db_users.find_one(
                    {
                        "pkey"  : token_data_get['user_id']
                    }
                )
                session['username'] = login_user['name']
                session['email']    = login_user['email']
                session['role']     = login_user['role'] 
                session['pkey']     = login_user['pkey']
                if session['role'] == 'admin':
                    response = {
                        'kboom' : 'UPLOAD_RAW'            
                    } 
                else:
                    response = 'dashboard'
            else:
                response = {
                "kboom" : "none",
                "message_error":"Token sudah deactive hufu",
                "number":"1"
            }
        else:
            response = {
                "kboom" : "none",
                "message_error":"Token INVALID HEHE",
                "number":"1"
            }
                            

        return response
    # end def
    
# end class
