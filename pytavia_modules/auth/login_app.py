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
       
        if login_user is not None:         
            self.webapp.logger.debug(login_user)     
            self.webapp.logger.debug("--------------true------------")        
            if bcrypt.hashpw(data['pass'].encode('utf-8'),login_user['password']) == login_user['password']:
                
                session['username'] = login_user['name']
                session['email']    = login_user['email']
                session['role']     = login_user['role'] 

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
    
# end class
