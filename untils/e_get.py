import json
import jsonpath


def get_json(case,r,allr):
    for key,value in json.loads(case['extract']).items():
        extract = jsonpath.jsonpath(r.json(),value)
        allr[key] = extract[0]
    return allr
