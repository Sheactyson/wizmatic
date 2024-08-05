import cv2
import urllib.request
import numpy as np

def pullImage(url):
    req = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1) # 'Load it as it is'

    cv2.imwrite("foundImage.png", img)