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

sys.path.append("pytavia_core")
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib")
sys.path.append("pytavia_storage")
sys.path.append("pytavia_modules")
sys.path.append("pytavia_modules")


from flask             import render_template_string
from flask             import render_template
from flask             import request

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

class save_content:    
    mgdDB = database.get_db_conn(config.mainDB)   
    sched = BackgroundScheduler()  
    sched.start()       

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


        title             = data["title"]
        content           = data["content"]
        start_date        = data["start_date"]
        end_date          = data["end_date"]      
        status_content    = 'inactive'          

        mdl_add_content = database.new(
            self.mgdDB , "db_content_management"
        )
        mdl_add_content.put( "title" , title)
        mdl_add_content.put( "content" , content)
        mdl_add_content.put( "start_date", start_date )
        mdl_add_content.put( "end_date" , end_date )
        mdl_add_content.put( "status_content" , status_content )

        db_handle  = database.get_database( config.mainDB )
        bulk_multi = bulk_db_multi.bulk_db_multi({
            "db_handle" : db_handle,
            "app"       : self.webapp
        })
        bulk_multi.add_action(
            bulk_db_multi.ACTION_INSERT ,
            mdl_add_content
        )

        bulk_multi.execute({})

        last_record    = self.mgdDB.db_content_management.find(
            {
                "status": {"$not":{"$regex":"DEACTIVE"}},
            }
        ).sort([("rec_timestamp_str" , -1)]).limit(1)
        
        last_record    = list( last_record )
        
        pkey        = last_record[0]['pkey']
        start_date  = last_record[0]['start_date']
        end_date    = last_record[0]['end_date']

        # start start-date cronjob
        y = self.loop_scheduler_start(pkey,start_date)  
        # end end-date cronjob   
        # start start-date cronjob
        y = self.loop_scheduler_end(pkey,end_date)  
        # end end-date cronjob   
        
        response = {
            'menu_value' : 'MANAGE_CONTENT'
        }

        return response
    # end def

    def loop_scheduler_start(self,pkey,start_date):        
        x = self.sched.add_job(self.temp_scheduler,'date', run_date=start_date, args=[{'pkey':pkey,'status_content':'live'}], replace_existing=True)        
    # end def

    def loop_scheduler_end(self,pkey,end_date):        
        x = self.sched.add_job(self.temp_scheduler,'date', run_date=end_date, args=[{'pkey':pkey,'status_content':'expired'}], replace_existing=True)        
    # end def

    def temp_scheduler(self,args):          
        self.mgdDB.db_content_management.update_one(
            { "pkey"          : args['pkey']},
            { "$set"          : { "status_content"   : args['status_content'] }} 
        )
    # end def
    
# end class
