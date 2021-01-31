import urllib
import urllib.request
import jsonlib
from model import ImshowModel
import base64


class ServerProxy:
    def __init__(self, baseUrl):
        self.baseUrl = "http://"+baseUrl

    def imshow(self, name, datas, waitTime=1):
        imshowModel = ImshowModel()
        imshowModel.name = name
        imshowModel.waitTime = waitTime
        imshowModel.datas = base64.b64encode(datas).decode('utf-8')
        jsonDatas = jsonlib.JsonSerialize().encode(
            imshowModel).encode(encoding="utf-8")
        try:
            response = urllib.request.urlopen(
                self.baseUrl + "/api/imshow", data=jsonDatas)
            if response.status != 200:
                print("request faild",
                      response.reason, response.status)
        except Exception as ex:
            print("request faild", ex, self.baseUrl + "/api/imgshow")
