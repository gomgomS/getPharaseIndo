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

class register_app:    
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
        
        data = request.form
        
        #start check existing user
        existing_user    = self.mgdDB.db_users.find_one(
            {
                "status": {"$not":{"$regex":"DEACTIVE"}},
                "$or"   :[{
                            "name"  : data['username']
                        },
                        {
                        "email" : data['email']
                    }
                ]
            }
        )
        
        #end check existing user

        if existing_user is None:
            #start save new user register to database
            hashpass = bcrypt.hashpw(data['pass'].encode('utf-8'),bcrypt.gensalt()) #enkrip pass
                        
            username        = data["username"]
            email           = data["email"]
            password        = hashpass
            role            = data["role"]                    

            mdl_add_user = database.new(
                self.mgdDB , "db_users"
            )
            mdl_add_user.put( "name" , username)
            mdl_add_user.put( "email" , email)
            mdl_add_user.put( "password", password )
            mdl_add_user.put( "role" , role )            

            db_handle  = database.get_database( config.mainDB )
            bulk_multi = bulk_db_multi.bulk_db_multi({
                "db_handle" : db_handle,
                "app"       : self.webapp
            })
            bulk_multi.add_action(
                bulk_db_multi.ACTION_INSERT ,
                mdl_add_user
            )

            bulk_multi.execute({})
            #end save

            #start save session
            session['username'] = username
            session['role'] = role
            #end save session            
            return "datanya berhasil didaftarkan"  
        return  "datanya sudah ada"
        
        response = {
            'menu_value' : 'MANAGE_CONTENT'
        }

        return response
    # end def
    
# end class
