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
import os

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

class generate_token:    
    mgdDB = database.get_db_conn(config.mainDB)         

    def __init__(self, app):
        self.webapp = app        
    # end def

    def process(self, params):        
        response = helper.response_msg(
            "CREATE_COMPANY_SUCCESS",
            "CREATE COMPANY SUCCESS", {},
            "0000"
        )  
      
        self.webapp.logger.debug(params)
        data = params
        self.webapp.logger.debug("------------------ddd")

        user_id             = data["user_id"]
        start_datetime      = data["start_datetime"]
        end_datetime        = data["end_datetime"]      
        tipe_token          = data["tipe_token"]   
        status_token        = 'active'   
        token               = data["token"]   
               
        mdl_add_tokenData = database.new(
            self.mgdDB , "db_token_access"
        )
        mdl_add_tokenData.put( "user_id", user_id                )
        mdl_add_tokenData.put( "start_datetime", start_datetime  )
        mdl_add_tokenData.put( "end_datetime", end_datetime      )
        mdl_add_tokenData.put( "tipe_token", tipe_token          )
        mdl_add_tokenData.put( "status_token", status_token      )
        mdl_add_tokenData.put( "token", token                    )

        db_handle  = database.get_database( config.mainDB )
        bulk_multi = bulk_db_multi.bulk_db_multi({
            "db_handle" : db_handle,
            "app"       : self.webapp
        })
        bulk_multi.add_action(
            bulk_db_multi.ACTION_INSERT ,
            mdl_add_tokenData
        )

        bulk_multi.execute({})
     
        
        response = {
            'kboom' : 'LIST_USER'
        }

        return response
    # end def    

    def _deactive(self, params):        
        response = helper.response_msg(
            "CREATE_COMPANY_SUCCESS",
            "CREATE COMPANY SUCCESS", {},
            "0000"
        )  
      
        self.webapp.logger.debug(params)
        
        x = self.mgdDB.db_token_access.update_one(
            { "pkey"          : params['id'] },
            {'$set':  {"status_token":'deactive'}  }
        )     
        
        response = {
            'kboom' : 'LIST_USER'
        }

        return response
    # end def    
# end class
