import sdk.jsonlib
from sdk.model import ImshowModel
from flask import Flask, request
import cv2
import numpy
import base64
import queue
import threading


app = Flask(__name__)


class Handle:
    def __init__(self):
        self.imgQueue = queue.Queue()
        threading.Thread(target=self.start).start()

    def start(self):
        while True:
            imshowModel = self.imgQueue.get()

            img_data = base64.b64decode(imshowModel.datas)
            imgArray = numpy.frombuffer(img_data, numpy.uint8)
            mat = cv2.imdecode(imgArray, cv2.IMREAD_ANYCOLOR)

            cv2.namedWindow(imshowModel.name, cv2.WINDOW_NORMAL)
            cv2.imshow(imshowModel.name, mat)
            cv2.waitKey(imshowModel.waitTime)


handles = {}  # type:dict[str,Handle]


@app.route('/api/imshow', methods=['POST'])
def imshow():
    imshowModel = ImshowModel()
    sdk.jsonlib.deserialize(imshowModel, request.get_data())
    if imshowModel.name in handles:
        handle = handles[imshowModel.name]
        handle.imgQueue.put(imshowModel)
    else:
        handle = Handle()
        handles[imshowModel.name] = handle
        handle.imgQueue.put(imshowModel)

    return ""


if __name__ == '__main__':
    app.run('0.0.0.0', 9999, debug=False)
