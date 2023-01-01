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
from flask             import session

from pytavia_stdlib    import idgen
from pytavia_stdlib    import utils
from pytavia_core      import database
from pytavia_core      import config
from pytavia_core      import helper
from pytavia_core      import bulk_db_insert
from pytavia_core      import bulk_db_update
from pytavia_core      import bulk_db_multi

class dashboard:
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
        launcher_content = 'dashboard.html'
        username = session.get('username')
        email    = session.get('email')
        role     = session.get('role')

        data_user    = self.mgdDB.db_users.find_one(
            {
                'name' : username,
                'email' : email
                #  "role": {"$not":{"$regex":"admin"}}
                # "status_content": 'expired'
            },{"_id":0,"password":0}
        ) 
        
        data_token_all = []
        
        token_data_get     = self.mgdDB.db_token_access.find(
            {
                "user_id": data_user['pkey']
                # "status_content": 'expired'
            },{"_id":0,"user_id":0,"rec_timestamp":0,'ipkey':0,'pkey':0}
        ) 
        self.webapp.logger.debug(token_data_get)
        data_user['token_data'] = list(token_data_get)

        ALL_DATA     = data_user 
            
        response = render_template(
            launcher_content,
            ALL_DATA = ALL_DATA,
            name = username,
            email = email,
            role = role,
            # ALL_DATA = ALL_DATA
        )

        return response
    # end def
# end class
