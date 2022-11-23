"""
# python3.6
import cgi , cgitb


def clean_html_dic(params):
    for index,item in params.items():
        if isinstance(item,str):
            params[index] = cgi.escape(item)
        #end if
    #end for
    return params
#end def

def clean_html(param):
    clean_param = cgi.escape(param)
    return clean_param
#end def
"""

# python3.8
import html


def clean_html_dic(params):
    for index,item in params.items():
        if isinstance(item,str):
            params[index] = html.escape(item)
        #end if
    #end for
    return params
#end def

def clean_html(param):
    clean_param = html.escape(param)
    return clean_param
#end def
