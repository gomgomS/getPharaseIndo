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
        
        manage_content_view  = self.mgdDB.db_scripts.find({},{'_id':0,'title_movie':1,'scene_name':1,'startTime':1,'endTime':1,'ref':1})             
        ALL_DATA     = list( manage_content_view )

        response = render_template(
            "front_page.html",
            ALL_DATA = ALL_DATA
        )
        self.webapp.logger.debug( "-----------------------------eee" )
        return response
    # end def
# end class
