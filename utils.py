# coding=utf-8

import json

def loads_json(js_ctx):
    js_dict = None
    try:
        js_dict = json.loads(js_ctx)
    except Exception as e:
        print(e)

    return js_dict