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

class view_content:
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
        data = params

        content = data.get('kboom')
        
        if content == 'MANAGE_CONTENT':
            launcher_content = 'manage_content.html'
            manage_content_view     = self.mgdDB.db_content_management.find(
                {
                    "status": {"$not":{"$regex":"DEACTIVE"}},
                    "status_content": 'inactive'
                }
            )             
            ALL_DATA     = list( manage_content_view )
        elif content == 'LIST_LIVE_CONTENT':
            launcher_content = 'list_live_content.html'
            manage_content_view     = self.mgdDB.db_content_management.find(
                {
                    "status": {"$not":{"$reg ":"DEACTIVE"}},
                    "status_content": 'live'
                }
            )   
            ALL_DATA     = list( manage_content_view )
        elif content == 'LIST_END_CONTENT':
            launcher_content = 'list_end_content.html'            
            manage_content_view     = self.mgdDB.db_content_management.find(
                {
                    "status": {"$not":{"$regex":"DEACTIVE"}},
                    "status_content": 'expired'
                }
            ) 
            ALL_DATA     = list( manage_content_view )
        elif content == 'UPLOAD_RAW':
            launcher_content = 'manage_video/upload_raw.html'            
            # manage_content_view     = self.mgdDB.db_content_management.find(
            #     {
            #         "status": {"$not":{"$regex":"DEACTIVE"}},
            #         "status_content": 'expired'
            #     }
            # ) 
            ALL_DATA     = []
        elif content == 'LIST_VIDEO':
            launcher_content = 'manage_video/list_video.html'            
            manage_content_view     = self.mgdDB.db_data_video.find(
                {
                    # "status": {"$not":{"$regex":"DEACTIVE"}},
                    # "status_content": 'expired'
                }
            ) 
            ALL_DATA     = list( manage_content_view )
        else:
            launcher_content = 'view_content.html'
            ALL_DATA = []

        
        

        
        response = render_template(
            launcher_content,
            ALL_DATA = ALL_DATA
        )

        return response
    # end def
# end class
