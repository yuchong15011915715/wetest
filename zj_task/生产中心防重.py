import threading
import time
import unittest
from zjtest_utils import new_uac_get_access_token_qa
import requests

uac_user = [{"username": "15011915715", "password": "Aa123456"},
            {"username": "13800000001", "password": "123456"},
            {"username": "13512340001", "password": "123456"}]


def get_uac_token_mps():
    uac_token = new_uac_get_access_token_qa('15011915715', 'Aa123123')
    print(uac_token)
    login_info = str(uac_token).split(",")
    return login_info


login_info = get_uac_token_mps()
accessToken = login_info[0]
userId = login_info[1]

# 产成品发货单审核
def t_shipmentsOrde_audit(args):

    url = 'https://qa-a.szzhijing.com/plmz-osp-mps/shipOrder/audit/1553988086299484162'
    data = {
    }

    header = {
        "Content-Type": "application/json",
        "accessToken": accessToken,
        "clientId": "FA98280021E64E8D9B8226E40E0151D7",
        "userId": userId
    }

    req = requests.post(url=url, headers=header, json=data).json()
    print(req)


if __name__ == '__main__':
    # t_shipmentsOrde_audit()
    thread1 = threading.Thread(target=t_shipmentsOrde_audit,args=("thread1",))
    thread2 = threading.Thread(target=t_shipmentsOrde_audit,args=("thread2",))
    thread1.start()
    time.sleep(1)
    thread2.start()