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
        # manage_content_view     = self.mgdDB.db_content_management.find(
        #     {
        #         "status": {"$not":{"$regex":"DEACTIVE"}},
        #         "status_content": 'live'
        #     }
        # )   
        # ALL_DATA     = list( manage_content_view )
            
        response = render_template(
            launcher_content,
            name = username,
            email = email,
            role = role,
            # ALL_DATA = ALL_DATA
        )

        return response
    # end def
# end class
