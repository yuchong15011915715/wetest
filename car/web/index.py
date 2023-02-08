from django.http import JsonResponse
from django.shortcuts import render
import os
import cv2
import imghdr
import time
import numpy as np
from tensorflow import keras

from django.views.decorators.csrf import csrf_exempt

from car.util.CNN import cnn_predict
from car.util.Unet import unet_predict
from car.util.core import locate_and_correct

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


"""
django-admin startproject car
manage.py runserver 0.0.0.0:8000
"""

MEDIA_ROOT = os.path.join(BASE_DIR, 'h5')

location = keras.models.load_model(os.path.join(MEDIA_ROOT, 'location.h5'))  # 车牌定位
cnn = keras.models.load_model(os.path.join(MEDIA_ROOT, 'cnn.h5'))  # 车牌识别


def main(request):
    context = {'content': "车牌识别"}
    return render(request, 'index.html',  context)


@csrf_exempt
def upload(request):
    try:
        my_file = request.FILES.get("licensePlate", None)
        if my_file:
            path = os.path.join(BASE_DIR, 'images')
            suffix = my_file.name.split(".")[1]
            file_name = (str(round(time.time() * 1000000)))+'.'+suffix
            image_path = os.path.join(path, file_name)
            destination = open(image_path,
                               'wb+')
            for chunk in my_file.chunks():
                destination.write(chunk)
            destination.close()
            imgType_list = {'jpg', 'bmp', 'png', 'jpeg', 'rgb', 'tif'}
            if imghdr.what(image_path) in imgType_list:
                license_plate = correct(image_path)
                return JsonResponse({'status': True, 'license_plate': license_plate},
                                    json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse({'status': False, 'msg': u'错误：文件类型不对额'},
                                    json_dumps_params={'ensure_ascii': False})

        else:
            return JsonResponse({'status': False, 'msg': u'错误：文件不存在'}, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        return JsonResponse({'status': False, 'msg': u'错误：{}'.format(e)}, json_dumps_params={'ensure_ascii': False})


def correct(image_path):
    img_src = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)  # 从中文路径读取时用
    h, w = img_src.shape[0], img_src.shape[1]
    if h * w <= 240 * 80 and 2 <= w / h <= 5:  # 满足该条件说明可能整个图片就是一张车牌,无需定位,直接识别即可
        lic = cv2.resize(img_src, dsize=(240, 80), interpolation=cv2.INTER_AREA)[:, :, :3]  # 直接resize为(240,80)
        img_src_copy, Lic_img = img_src, [lic]
    else:  # 否则就需通过unet对img_src原图预测,得到img_mask,实现车牌定位,然后进行识别
        img_src, img_mask = unet_predict(location, image_path)
        img_src_copy, Lic_img = locate_and_correct(img_src, img_mask)  # 利用core.py中的locate_and_correct函数进行车牌定位和矫正

    Lic_predict = cnn_predict(cnn, Lic_img)  # 利用cnn进行车牌的识别预测,Lic_pred中存的是元祖(车牌图片,识别结果)
    license_plate = ""
    if Lic_predict:
        for i, lic in enumerate(Lic_predict):
            if i == 0:
                license_plate = lic[1]
            elif i == 1:
                license_plate = lic[1]
            elif i == 2:
                license_plate = lic[1]
        print("车牌号：" + license_plate)
    else:  # Lic_predict 为空说明未能识别
        print("未能识别")
    return license_plate


if __name__ == '__main__':
    img_path = "c:\\01.jpg"
    correct(img_path)

