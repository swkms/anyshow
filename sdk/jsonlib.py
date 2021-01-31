import json
import array
import base64
import copy

class JsonSerialize(json.JSONEncoder):
    def default(self, obj):
        d = {}
        d.update(obj.__dict__)
        return d


def _deserializeObj(obj, dic):
    newDic = {}
    for (key, value) in dic.items():
        newDic[key.lower()] = value
    for member in dir(obj):
        if (member[0] == "_"):
            continue
        value = newDic.get(member.lower())
        if value is not None:
            if isinstance(getattr(obj, member), bytearray):
                setattr(obj, member, bytearray(base64.decodestring(value)))
            else:
                setattr(obj, member, value)
    return obj


def deserialize(obj, content):
    if content == "":
        return None
    jsonStr = ""
    if (isinstance(content, bytearray)):
        jsonStr = content.decode("utf-8")
    else:
        jsonStr = content
    dics = json.loads(jsonStr)
    if (isinstance(dics, list)):
        array = []
        for item in dics:
            netObj = copy.copy(obj)
            d = _deserializeObj(netObj, item)
            array.append(d)
        return array
    return _deserializeObj(obj, dics)
