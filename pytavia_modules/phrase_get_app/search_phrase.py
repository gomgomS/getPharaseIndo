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

class search_phrase:
    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def search(self, params):
        ALL_DATA     = 'haii'
        
        self.webapp.logger.debug( params )
        

        if params.get('search-keyword') is None:
            manage_content_view  = self.mgdDB.db_scripts.find({},{'_id':0,'title_movie':1,'scene_name':1,'startTime':1,'endTime':1,'ref':1})
        # else:
        #     self.webapp.logger.debug( "BELUM" )
        #     search_keyword = params['search-keyword']
        #     search_figure_keyword = params['search-figure-keyword']
        #     self.webapp.logger.debug(search_figure_keyword == '')
        #     self.webapp.logger.debug( search_keyword)
        #     manage_content_view  = self.mgdDB.db_scripts.find({},{'$text':{'$search':'\"'+search_keyword+'\" '}},
        #                                 {'_id':0,'title_movie':1,'scene_name':1,'startTime':1,'endTime':1,'ref':1}).sort([("startTime", pymongo.ASCENDING)])
        else:
            search_keyword        = params['search-keyword']
            search_figure_keyword = params['search-figure-keyword']

            if search_keyword != "" and search_figure_keyword == "":
                self.webapp.logger.debug( "BELUM" )
            
                self.webapp.logger.debug(search_figure_keyword == '')
                self.webapp.logger.debug( search_keyword)
                manage_content_view  = self.mgdDB.db_scripts.find({'$text':{'$search':'\"'+search_keyword+'\" '}},
                                            {'_id':0,'title_movie':1,'scene_name':1,'startTime':1,'endTime':1,'ref':1}).sort([("startTime", pymongo.ASCENDING)])
            else:
                # 3 if filter only keyword figure 
                filter = {}
                self.webapp.logger.debug( "HIAAAAAAAAAAAAAAAAAAAAAAAA" )
                if search_figure_keyword != "":                    
                    list_data_video  = self.mgdDB.db_data_video.find({'$text':{'$search':search_figure_keyword}},
                                            {'_id':0,'focus_figure':1,'id_upload':1}).sort([("startTime", pymongo.ASCENDING)])
                    arr = []
                    for data in list_data_video:
                        arr.append(data['id_upload'])
                    
                    # self.webapp.logger.debug(arr)
                    
                    filter['id_upload'] = {'$in' : arr }

                if search_keyword != ""       : filter['ref']       = {'$regex' : search_keyword }

                manage_content_view  = self.mgdDB.db_scripts.find(filter,{'_id':0,'title_movie':1,'scene_name':1,'startTime':1,'endTime':1,'ref':1}).sort([("startTime", pymongo.ASCENDING)])
           
                self.webapp.logger.debug("-------------------------------")
        # s elf.webapp.logger.debug(list(manage_content_view))
        ALL_DATA     = list( manage_content_view )

        response = render_template(
            "front_page.html",
            ALL_DATA = ALL_DATA
        )
        return response
    # end def
# end class
