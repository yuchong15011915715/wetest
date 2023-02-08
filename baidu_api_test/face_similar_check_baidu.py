# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 15:13:18 2018

@author: Administrator
"""
import time
from os import listdir
import os
import urllib3, base64, json

import warnings

warnings.filterwarnings("ignore")

# import urllib  # , urllib2, sys
import cv2
import requests


# client_id 为官网获取的AK， client_secret 为官网获取的SK

def get_access_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=G0ZuAQrV9C6A0aSfpgUgdRla&client_secret=lKitrgwxOhmf9WzOzhIccxvx2KBvEgPz'
    request__header = {'Content-Type': "application/json; charset=UTF-8"}
    result = requests.get(host, headers=request__header).json()
    print(result)
    return result['access_token']


def Remove_duplicate():
    access_token = get_access_token()
    http = urllib3.PoolManager(num_pools=4)
    IMAGE_TYPE = 'BASE64'
    url = 'https://aip.baidubce.com/rest/2.0/face/v3/match?access_token=' + access_token
    while True:
        dirName = "C:\\Users\\ZJ\Pictures\\Camera Roll\\"  # 相册路径
        # 获取文件内的所有的文件  list
        dirList = listdir(dirName)  # 相册名
        for i in dirList:
            if (os.path.exists('C:\\Users\\ZJ\Pictures\\Camera Roll\\%s' % (str(i)))):
                for j in dirList[:20]:
                    if (i != j):
                        im = r'%s\%s' % (dirName, str(i))
                        ib = r'%s\%s' % (dirName, str(j))
                        f1 = open(im, 'rb')
                        f2 = open(ib, 'rb')
                        # 参数image：图像base64编码 分别base64编码后的2张图片数据
                        img1 = base64.b64encode(f1.read())
                        img2 = base64.b64encode(f2.read())
                        f1.close()
                        f2.close()
                        # params = {"images":str(img1,'utf-8') + ',' + str(img2,'utf-8')}
                        params = [{"image": str(img1, 'utf-8'), "image_type": IMAGE_TYPE},
                                  {"image": str(img2, 'utf-8'), "image_type": IMAGE_TYPE}]
                        # 参数转JSON格式
                        encoded_data = json.dumps(params).encode('utf-8')
                        request = http.request('POST',
                                               url,
                                               body=encoded_data,
                                               headers={'Content-Type': 'application/json'})
                        # 对返回的byte字节进行处理。Python3输出位串，而不是可读的字符串，需要进行转换
                        result = str(request.data, 'utf-8')
                        result = json.loads(result)
                        print(result)
                        time.sleep(1)
                        if result['error_code'] != 0:
                            print(j)
                            print(str(result['error_msg']))
                            os.remove('C:\\Users\\ZJ\Pictures\\Camera Roll\\%s' % (str(j)))
                            dirList = listdir(dirName)
                            continue
                        # print(result)
                        time.sleep(1)
                        print('The similarity between %s and %s is %f' % (str(i), str(j), result['result']['score']))
                        print()
                        if result['result']['score'] >= 45:
                            # print('The similarity between %s and %s is %f'%(str(i),str(j),result['result']['score']))
                            os.remove('C:\\Users\\ZJ\Pictures\\Camera Roll\\%s' % (str(j)))
                            dirList = listdir(dirName)
            if (os.path.exists('C:\\Users\\ZJ\Pictures\\Camera Roll\\%s' % (str(i)))):
                print("Yes")
                img = cv2.imread("C:\\Users\\ZJ\Pictures\\Camera Roll\\%s" % (str(i)))
                # if(img.any()):
                # print("Yes")
                cv2.imwrite("./face_pictures_/%s" % (str(i)), img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                os.remove('C:\\Users\\ZJ\Pictures\\Camera Roll\\%s' % (str(i)))
                break


if __name__ == '__main__':
    Remove_duplicate()
