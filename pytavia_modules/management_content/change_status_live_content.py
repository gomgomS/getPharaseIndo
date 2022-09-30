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

class change_status_live_content:    
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
        
        data = request.form        
        if str(data.get('change-status-expired')) != 'None':
            self.mgdDB.db_content_management.update_one(
                { "pkey"          : data['change-status-expired'] },
                { "$set"          : { "status_content"   : "expired" }} 
            ) 
            url = 'LIST_LIVE_CONTENT'
        else:    
            self.mgdDB.db_content_management.update_one(
                { "pkey"          : data['change-status'] },
                { "$set"          : { "status_content"   : "live" }} 
            ) 
            url = 'MANAGE_CONTENT'
        
        response = {
            'menu_value' : url
        }

        return response
    # end def    
# end class
