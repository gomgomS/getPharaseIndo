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

class delete_video_data:    
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
        id_upload = params['delete']
        self.webapp.logger.debug(id_upload)
        self.webapp.logger.debug("------------------ddd")

        list_name_video = self.mgdDB.db_scripts.find({
            "id_upload"   : id_upload
        },{'_id':0,'title_movie':0,'startTime':0,'endTime':0,'ref':0})
        
        list_all_data_video = list(list_name_video )

        # delete video from storage
        for data in list_all_data_video:
            isExist = os.path.exists(config.G_STORAGE_PATH+'/'+data['scene_name'])
            if isExist:
                os.remove(config.G_STORAGE_PATH+'/'+data['scene_name'])
        # end for

         # delete video list script
        query_db_scripts  = {"id_upload":id_upload}
        delete_result = self.mgdDB.db_scripts.delete_many(query_db_scripts)

        # delete from list data movie
        x = self.mgdDB.db_data_video.delete_one(
            { "id_upload"          : id_upload }   
        )  
     
        
        response = {
            'kboom' : 'LIST_VIDEO'
        }

        return response
    # end def    
# end class
