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
import re
import pathlib
import uuid


sys.path.append("pytavia_core")
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib")
sys.path.append("pytavia_storage")
sys.path.append("pytavia_modules")
sys.path.append("pytavia_modules")


from flask             import render_template_string
from flask             import render_template
from flask             import request
from pathlib           import Path
from moviepy.editor    import VideoFileClip

from pytavia_stdlib    import idgen
from pytavia_stdlib    import utils
from pytavia_core      import database
from pytavia_core      import config
from pytavia_core      import helper
from pytavia_core      import bulk_db_insert
from pytavia_core      import bulk_db_update
from pytavia_core      import bulk_db_multi

class split_raw_phrase:
    mgdDB = database.get_db_conn(config.mainDB)

    def __init__(self, app):
        self.webapp = app
    # end def

    def _split_scripts_movie(self, params):
        regex = r'(?:\d+)\s(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)\s+(.+?)(?:\n\n|$)'
        offset_seconds = lambda ts: sum(howmany * sec for howmany, sec in zip(map(int, ts.replace(',', ':').split(':')), [60 * 60, 60, 1, 1e-3]))

        full_movie  = config.G_UPLOAD_PATH+'/gundala.srt'
        title_movie = Path(full_movie).stem
        transcript   = [dict(scene_name = str(uuid.uuid1())+'.mp4', title_movie = title_movie, startTime = offset_seconds(startTime), endTime = offset_seconds(endTime), ref = ' '.join(ref.split())[22:-7].replace('"', '')) for startTime, endTime, ref in re.findall(regex, open(full_movie).read(), re.DOTALL)]
       
        # print(json.dumps(transcript,indent=2))
        # print(Path(full_movie).stem)
 
        self.webapp.logger.debug(type(transcript))
        # x = self.mgdDB["db_scripts"]
        # x.insert_many(transcript)
        return transcript
        # return transcript
    
    def _split_scene_movie(self, params):
        temp = self._split_scripts_movie(params) 
        return temp
  
        for idx,script_detail in enumerate(temp):
            start_in_second = script_detail['startTime']
            end_in_second = script_detail['endTime']

            full_movie  = config.G_STORAGE_PATH+'/gundala.mkv'
            clip = VideoFileClip(full_movie).subclip(start_in_second,end_in_second)
            clip.write_videofile(config.G_STORAGE_PATH+'/'+script_detail['scene_name'], fps=30, threads=1, codec="libx264")
        return 'lets check it'
# end class
