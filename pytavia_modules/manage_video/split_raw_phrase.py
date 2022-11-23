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

import os
from werkzeug.utils import secure_filename

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

    def _cleanse_data(self,params):
        
        focus_figure           = params["focus_figure"]
        video_source           = params["video_source"]

        files_subtitle         = params["files"]["subtitle"]
        files_movie            = params["files"]["movie"]
        self.webapp.logger.debug(params)
        id_upload              = str(uuid.uuid1())
        filename = secure_filename(files_subtitle.filename)
        filename_movie = secure_filename(files_movie.filename)
        
        files_subtitle.save(os.path.join(config.G_UPLOAD_PATH, filename))
        files_movie.save(os.path.join(config.G_UPLOAD_PATH, filename_movie))
        
        #check if data already input or not
        check  = self.mgdDB.db_data_video.find_one({'$text':{'$search':'\"'+filename+'\" '}})
        self.webapp.logger.debug(check)
        if check is not None:
            return check['title'] + ' sudah ada'
      
        #input database
        x = self.mgdDB["db_data_video"]

        # title movie from title script subtile
        mdl_add_content = {}
        mdl_add_content["title"] = filename
        mdl_add_content["focus_figure"] = focus_figure
        mdl_add_content["video_source"] = video_source
        mdl_add_content["id_upload"] = id_upload
        x.insert_one(mdl_add_content)

        # split srt subtitle file
        params['subtitle_name'] = filename
        params['id_upload']     = id_upload
        script_result = self._split_scripts_movie(params) 
       
        # split video file
        params['subtitle_movie'] = filename_movie
        scene_result = self._split_scene_movie(script_result,params) 

        return scene_result

    def _split_scripts_movie(self, params):
        regex = r'(?:\d+)\s(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)\s+(.+?)(?:\n\n|$)'
        offset_seconds = lambda ts: sum(howmany * sec for howmany, sec in zip(map(int, ts.replace(',', ':').split(':')), [60 * 60, 60, 1, 1e-3]))

        full_movie  = config.G_UPLOAD_PATH +'/'+ params['subtitle_name']
        title_movie = Path(full_movie).stem
        # transcript   = [dict(scene_name = str(uuid.uuid1())+'.mp4', title_movie = title_movie, startTime = offset_seconds(startTime), endTime = offset_seconds(endTime), ref = ' '.join(ref.split())[22:-7].replace('"', ''),) for startTime, endTime, ref in re.findall(regex, open(full_movie).read(), re.DOTALL)]
        transcript   = [dict(id_upload =params['id_upload'], scene_name = str(uuid.uuid1())+'.mp4', title_movie = title_movie, startTime = offset_seconds(startTime), endTime = offset_seconds(endTime), ref = ref) for startTime, endTime, ref in re.findall(regex, open(full_movie).read(), re.DOTALL)]
        print(json.dumps(transcript,indent=2))
        print(Path(full_movie).stem)
 
        self.webapp.logger.debug(type(transcript))
        x = self.mgdDB["db_scripts"]
        x.insert_many(transcript)
        return transcript

    def _split_scene_movie(self,script_result, params):
        result = 'SUCCES'
        for idx,script_detail in enumerate(script_result):
            start_in_second = script_detail['startTime']
            end_in_second = script_detail['endTime']

            full_movie  = config.G_UPLOAD_PATH +'/'+ params['subtitle_movie']
            #cut the video by data
            clip = VideoFileClip(full_movie).subclip(start_in_second,end_in_second)
            #resize the video because to big
            clip = clip.resize(0.3)
            clip.write_videofile(config.G_STORAGE_PATH+'/'+script_detail['scene_name'], fps=30, threads=1, codec="libx264")
      

        return result
# end class
