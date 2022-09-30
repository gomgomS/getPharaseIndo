import json
import time
import pymongo
import sys
import urllib.parse
import base64
import time

sys.path.append("pytavia_core"    )
sys.path.append("pytavia_settings")
sys.path.append("pytavia_stdlib"  )
sys.path.append("pytavia_storage" )
sys.path.append("pytavia_modules" )

from pytavia_core import pytavia_event_loop

class event_loop_proc(pytavia_event_loop.pytavia_event_loop):

    def __init__(self, params):
        pytavia_event_loop.pytavia_event_loop.__init__(self, params)
    # end def

    def execute(self, params):
        pytavia_event_loop.pytavia_event_loop.execute( self, params )
    # end def
# end class
