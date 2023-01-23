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
import glob

sys.path.append("pytavia_core")
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib")
sys.path.append("pytavia_storage")
sys.path.append("pytavia_modules")
sys.path.append("pytavia_modules")


from flask             import render_template_string
from flask             import render_template
from flask             import request
from flask             import redirect

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
        elif content == 'LIST_USER':
            launcher_content = 'manage_video/list_user.html'            
            manage_content_view     = self.mgdDB.db_users.find(
                {
                    #  "role": {"$not":{"$regex":"admin"}}
                    # "status_content": 'expired'
                },{"_id":0,"password":0}
            ) 

            data_token_all = []
            for each_content in manage_content_view:
                token_data_get     = self.mgdDB.db_token_access.find(
                    {
                        "user_id": each_content['pkey']
                        # "status_content": 'expired'
                    },{"_id":0}
                ) 
                each_content['token_data'] = list(token_data_get)
                data_token_all.append(each_content)


            
            ALL_DATA     = list( data_token_all )

        elif content == 'DELETE_FILE_UPLOAD_FOLDER':
            folder_path = config.G_UPLOAD_PATH
            for f in os.listdir(folder_path):
                 os.remove(os.path.join(folder_path, f))

            return 'success delete file in upload'

        elif content == 'DELETE_EVERY_SCRIPT_DONT_HAVE_VIDEO':
            folder_path = config.G_STORAGE_PATH
            data_storage = []
            for f in os.listdir(folder_path):
                data_storage.append(f)

            
            scripts_rec = self.mgdDB.db_scripts.find({},{'_id':0,'id_upload':0,'title_movie':0,'startTime':0,'endTime':0,'ref':0})

            i = 0
            # REMOVE DATA FROM SCRIPTS
            arr_scripts_rec = []
            for scr in scripts_rec:
                if scr['scene_name'] not in data_storage:
                    i += 1
                    delete_result_x = self.mgdDB.db_scripts.delete_one({'scene_name':scr['scene_name']})

                arr_scripts_rec.append(scr['scene_name'])

            y = 0
            # REMOVE VIDEO.MKV FROM STORAGE
            for data in data_storage:
                if data not in arr_scripts_rec:
                     y += 1
                     if data != 'loading.mkv':
                        os.remove(os.path.join(folder_path, data))



            return [data_storage,arr_scripts_rec,i,y]
        else:
            launcher_content = 'manage_video/upload_raw.html'            
            # manage_content_view     = self.mgdDB.db_content_management.find(
            #     {
            #         "status": {"$not":{"$regex":"DEACTIVE"}},
            #         "status_content": 'expired'
            #     }
            # ) 
            ALL_DATA     = []

        response = render_template(
            launcher_content,
            ALL_DATA = ALL_DATA
        )

        return response
    # end def
# end class
