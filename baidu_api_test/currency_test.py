import base64
import os.path
from os import listdir
from time import sleep

import requests
from face_similar_check_baidu import get_access_token

flag_time = False


def baidu_currency_api():
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/currency"
    # pic_file = open('D:\\Demo\\PythonDemo\\wetest\\pic\\img.png', 'rb')
    dir_name = "D:\\Demo\\PythonDemo\\wetest\\pic\\"
    access_token = get_access_token()
    # 获取当前文件夹下面所有的文件
    dir_list = listdir(dir_name)
    for i in dir_list:
        if os.path.exists(dir_name + '%s' % (str(i))):
            pic_file = open(dir_name + str(i), 'rb')
            img = base64.b64encode(pic_file.read())

            params = {'image': img}
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(request_url + "?access_token=" + access_token, data=params, headers=headers)
            result = response.json()
            # print(str(result))
            try:
                if result['result']['currencyName']:
                    print(str(i) + ":" + str(result['']))
                    sleep(2)
                else:
                    pass
            except:
                try:
                    if result["error_msg"]:
                        print(str(i) + ":" + str(result['error_msg']))
                        sleep(2)
                except:
                    pass


if __name__ == "__main__":
    baidu_currency_api()
