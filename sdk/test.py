from serverproxy import ServerProxy
import cv2
import time
if __name__ == '__main__':
    serverProxy = ServerProxy("localhost:9999")
    mat = cv2.imread("./1.jpg")
    _, datas = cv2.imencode(".jpg", mat)
    while True:
        serverProxy.imshow("TEST", datas, 3000)
        time.sleep(1)
    time.sleep(100000)
