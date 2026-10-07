from config.config import *



def use_data(data):
    method = data["method"]
    url = URL+data["path"]
    json_val = data["json"]
    if isinstance(json_val,str) and json_val not in ["","null"] :
        json_val = eval(json_val)
    else :
        json_val = None
    return{
        "method":method,
        "url":url,
        "json":json_val
    }


def use_goods(data):
    method = data["method"]
    url = URL+data["path"]
    json_val = data["json"]
    if isinstance(json_val,str) and json_val not in ["","null"] :
        json_val = json_val
    else :
        json_val = None
    return{
        "method":method,
        "url":url,
        "json":json_val
    }


