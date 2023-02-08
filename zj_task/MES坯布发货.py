import threading
import time
import unittest
from zjtest_utils import new_uac_get_access_token_uat
import requests



def notice_create():
    url = 'https://uat-a.szzhijing.com/woven/cloth/delivery/notice/create'
    data = {"handleDate": "2022-12-23", "saleOrder": "22-xxx001-24", "billType": 0, "billState": 0, "deliveryType": "0",
            "warehouseId": "53BEFA7BA63B40E3963C306AE712EC57", "warehouseName": "本厂仓库", "arrivalDate": "2022-12-31",
            "remark": "",
            "customer": {"deliveryIdentify": "906EE20747C24B679737FE7B9095E086", "delivery": "上海辰景信息科技有限公司",
                         "deliveryAddress": "宜宾原料仓", "deliveryAddressId": "1567826277318488065",
                         "deliveryAddressCode": "W10087", "contact": ""},
            "operator": {"handleUser": "余冲uat", "handleUserId": "76E0C0BD38414025A4E8DAD7B0958D9E",
                         "handleUserDate": "2022-12-23", "createUser": "余冲uat",
                         "createUserId": "446F7F89FDF1475A98BC89EB79B8FE3A", "createDate": "2022-12-23 16:55:11"},
            "detailList": [{"entityList": [{"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 0}},
                                           {"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 1}},
                                           {"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 2}},
                                           {"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 3}},
                                           {"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 4}}],
                            "materialId": "816996375505670144", "materialName": "75D半光平纹14/26捻银丝雪纺-1028",
                            "materialCode": "PBPQ15126001", "batchNo": "HZ001-PBPQ15126001-L3", "grade": "AA",
                            "existCount": 45, "existMainCount": 12, "existSecondCount": 0,
                            "warehouseId": "53BEFA7BA63B40E3963C306AE712EC57", "warehouseName": "本厂仓库",
                            "enquiryDate": "2022-12-31", "accessory": {
                    "imageUrl": "https://quanbu-woven-test.oss-cn-hangzhou.aliyuncs.com/0_1671785164271.png"}}, {
                               "entityList": [{"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 0}},
                                              {"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 1}},
                                              {"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 2}},
                                              {"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 3}},
                                              {"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 4}}],
                               "materialId": "816996375505670144", "materialName": "75D半光平纹14/26捻银丝雪纺-1028",
                               "materialCode": "PBPQ15126001", "batchNo": "HZ001-PBPQ15126001-K3", "grade": "AA",
                               "existCount": 44, "existMainCount": 170, "existSecondCount": 0,
                               "warehouseId": "53BEFA7BA63B40E3963C306AE712EC57", "warehouseName": "本厂仓库",
                               "enquiryDate": "2022-12-31", "accessory": {
                    "imageUrl": "https://quanbu-woven-test.oss-cn-hangzhou.aliyuncs.com/0_1671785188201.png"}}, {
                               "entityList": [{"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 0}},
                                              {"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 1}},
                                              {"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 2}},
                                              {"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 3}},
                                              {"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 4}}],
                               "materialId": "816996375505670144", "materialName": "75D半光平纹14/26捻银丝雪纺-1028",
                               "materialCode": "PBPQ15126001", "batchNo": "HZ001-PBPQ15126001-L3", "grade": "B",
                               "existCount": 50, "existMainCount": 500, "existSecondCount": 0,
                               "warehouseId": "53BEFA7BA63B40E3963C306AE712EC57", "warehouseName": "本厂仓库",
                               "enquiryDate": "2022-12-31", "accessory": {
                    "imageUrl": "https://quanbu-woven-test.oss-cn-hangzhou.aliyuncs.com/0_1671785200049.png"}}, {
                               "entityList": [{"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 0}},
                                              {"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 1}},
                                              {"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 2}},
                                              {"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 3}},
                                              {"mainCount": 1, "extendData": {"crosswiseNum": 0, "lengthwaysNum": 4}}],
                               "materialId": "816996375505670144", "materialName": "75D半光平纹14/26捻银丝雪纺-1028",
                               "materialCode": "PBPQ15126001", "batchNo": "HZ001-PBPQ15126001-J3", "grade": "B",
                               "existCount": 100, "existMainCount": 10000, "existSecondCount": 0,
                               "warehouseId": "53BEFA7BA63B40E3963C306AE712EC57", "warehouseName": "本厂仓库",
                               "enquiryDate": "2022-12-31", "accessory": {
                    "imageUrl": "https://quanbu-woven-test.oss-cn-hangzhou.aliyuncs.com/0_1671785218138.png"}}],
            "factoryId": "B7BD84C5B7D0481A8B140D8DE322D064"}

    header = {
        "Content-Type": "application/json",
        "accessToken": '926A7AEF621D4462B464FDB5CCE7D829',
        "clientId": "3200AE0DC06944A9A5BB4B81ACBF01BE",
        "userId": '446F7F89FDF1475A98BC89EB79B8FE3A',
        "orgCode": 'B7BD84C5B7D0481A8B140D8DE322D064',
    }

    req = requests.post(url=url, headers=header, json=data).json()
    print(req)
    deliveryNoticeId = req["result"]["deliveryNoticeId"]
    print(deliveryNoticeId)
    return deliveryNoticeId


def notice_create_2():
    deliveryNoticeId = notice_create()
    url_2 = 'https://uat-a.szzhijing.com/woven/cloth/delivery/notice/submit/' + str(deliveryNoticeId)
    header = {
        "Content-Type": "application/json",
        "accessToken": '926A7AEF621D4462B464FDB5CCE7D829',
        "clientId": "3200AE0DC06944A9A5BB4B81ACBF01BE",
        "userId": '446F7F89FDF1475A98BC89EB79B8FE3A',
        "orgCode": 'B7BD84C5B7D0481A8B140D8DE322D064',
    }
    data = {"factoryId": "B7BD84C5B7D0481A8B140D8DE322D064"}

    req = requests.post(url=url_2, headers=header, json=data).json()
    print(req)


if __name__ == '__main__':
    # for i in range(0,10):
    notice_create_2()
    # t_shipmentsOrde_audit()
    # thread1 = threading.Thread(target=audit_shippingNotice, args=("thread1",))
    # thread2 = threading.Thread(target=inboundOrder_saveAll, args=("thread2",))
    # thread1.start()
    time.sleep(1)
    # thread2.start()
