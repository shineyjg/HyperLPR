# -*- coding:utf-8 -*-
import os
import time
import json
import redis
import cv2
from hyperlpr_py3 import pipline as pp

def main():
    REDIS_EXPIRE = 10
    r = redis.Redis('localhost', 6379, password='Byte20171116@')

    while (True):
        print('wait to detect plate number!')
        filename = r.brpop('plate_recog')
        filename = bytes.decode(filename[1])
        # print('filename', filename)

        imgpath = os.path.join('../uploads', filename)
        # print('imgpath', imgpath)

        start = time.time()
        image = cv2.imread(imgpath)
        _, res = pp.SimpleRecognizePlate(image)
        print(res)
 
        r.expire(filename, REDIS_EXPIRE)
        r.lpush(filename, json.dumps({'status':0, 'plates': res}))


if __name__ == '__main__':
    main()
