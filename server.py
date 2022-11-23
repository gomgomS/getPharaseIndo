import json
import time
import pymongo
import sys
import urllib.parse
import base64
import html as html_unescape

sys.path.append("pytavia_core"    ) 
sys.path.append("pytavia_settings") 
sys.path.append("pytavia_stdlib"  ) 
sys.path.append("pytavia_storage" ) 
sys.path.append("pytavia_modules" ) 
sys.path.append("pytavia_modules/rest_api_controller")
sys.path.append("pytavia_modules/management_content") 
sys.path.append("pytavia_modules/phrase_get_app") 
sys.path.append("pytavia_modules/manage_video")

# adding comments
from pytavia_stdlib  import utils
from pytavia_core    import database 
from pytavia_core    import config 
from pytavia_core    import model

from pytavia_stdlib  import idgen 
from pytavia_stdlib  import sanitize

from rest_api_controller import module1 

from management_content import view_content
from management_content import save_content
from management_content import delete_content
from management_content import change_status_live_content
from management_content import news

from phrase_get_app     import search_phrase
from manage_video   import split_raw_phrase


##########################################################

from flask import request
from flask import render_template
from flask import Flask
from flask import session
from flask import make_response
from flask import redirect
from flask import url_for
from flask import flash


from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import CSRFError
#
# Main app configurations
#
app             = Flask( __name__, config.G_STATIC_URL_PATH )
# csrf            = CSRFProtect(app)
app.secret_key  = config.G_FLASK_SECRET
app.db_update_context, app.db_table_fks = model.get_db_table_paths(model.db)

# sched = BackgroundScheduler()    

########################## CALLBACK API ###################################

@app.route("/hi", methods=["GET"])
def api_hi():
    return 'dari mana'
# end def

@app.route("/his", methods=["GET"])
def api_hix():
    app.logger.debug('yeahhh')
    return 'ma brooo gloooo gl;oooo bro'
# end def

#START PHRASE_GET_APP
@app.route("/search", methods=["GET"])
def search():  
    params = request.args.to_dict()    
    response = search_phrase.search_phrase(app).search( params )
    return response
# end def

@app.route("/split_raw_phrase", methods=["POST"])
def split_phrase():  
    files                 = request.files
    params                = sanitize.clean_html_dic(request.form.to_dict())
    app.logger.debug("---------------param")
    app.logger.debug(params)
    # params                = sanitize.clean_html_dic(request.form.to_dict())
    # params["fk_user_id" ] = session.get("fk_user_id")
    params["files"      ] = files

    response = split_raw_phrase.split_raw_phrase(app)._cleanse_data( params )
    return response
# end def

@app.route("/search-script", methods=["GET"])
def search_script():    
    params = request.args.to_dict()    
    app.logger.debug("---------------param")
    app.logger.debug(params)
    response = search_phrase.search_phrase(app).search( params )
    return response
# end def

#END PHRASE_GET_APP

@app.route("/news", methods=["GET"])
def launch_news():  
    params = request.args.to_dict()    
    response = news.news(app).process( params )
    return response
# end def

@app.route("/what", methods=["GET"])
def content():  
    params = request.args.to_dict()    
    response = view_content.view_content(app).process( params )
    return response
# end def

@app.route("/what", methods=["GET"])
def content_direct(menu_value):  
    params = request.args.to_dict()    
    response = view_content.view_content(app).process( params )
    return response
# end def

@app.route("/save_content", methods=["POST"])
def save_content_data():
    params = request.args.to_dict()    
    response = save_content.save_content(app).process( params )           
    # temporari
    # sched.add_job(temp, run_date='2022-05-22 20:35:00')
    # sched.start()
    # end temp

    res = list(response.keys())[0]        
    return redirect(url_for('content_direct',menu_value=response[res]))  
    return response
# end def

@app.route("/delete", methods=["POST"])
def delete_content_data():  
    params = request.args.to_dict()    
    response = delete_content.delete_content(app).process( params )    
    res = list(response.keys())[0]  #take first key in list     
    return redirect(url_for('content_direct',menu_value=response[res]))      
# end def

@app.route("/change-status-live-content", methods=["POST"])
def change_status_live_content_data():  
    params = request.args.to_dict()    
    response = change_status_live_content.change_status_live_content(app).process( params )        
    res = list(response.keys())[0]  #take first key in list     
    return redirect(url_for('content_direct',menu_value=response[res]))      


@app.route("/formschedule", methods=["POST","GET"])
def form():
    params = request.args.to_dict()
    response = schedule_app.schedule_app(app).process( params )
    return response