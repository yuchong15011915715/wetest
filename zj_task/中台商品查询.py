from random import randint
from locust import HttpUser, between, SequentialTaskSet, task
from zj_task.zjtest_utils import uac_get_access_token, check

host_url = 'https://qa-a.szzhijing.com'
clientId = '50EECEB9F781417DA11B0D4EB55386D1'

is_check = True


class TaskCase(SequentialTaskSet):
    uac_user = [{"username": "15011915715", "password": "Aa123456"},
                {"username": "13800000001", "password": "123456"},
                {"username": "13512340001", "password": "123456"}]

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.ranIndex = randint(0, len(self.uac_user) - 1)

    @task(1)
    def get_list_page(self):
        print("----------------------" + str(self.ranIndex))
        user_info = self.uac_user[self.ranIndex]
        print("取出来的用户信息：" + user_info["username"] + "," + user_info["password"])
        uac_access_token = uac_get_access_token(user_info["username"],
                                                str(user_info["password"]).replace('\n', ''))
        login_info = str(uac_access_token).split(",")

        params = {
            "pageNum": 1,
            "pageSize": 30,
            "categoryId": "557590419822628888"
        }
        header = {"Content-Type": "application/json",
                  "authen-type": "V2",
                  "clientId": clientId,
                  "accessToken": login_info[0],
                  "userId": login_info[1],
                  "orgCode": "4D17A04844B84A898F22F233172AE873"
                  }
        req = self.client.get("/boc/goods/products/v2/page", headers=header, params=params)
        check(req, is_check)


class UacLogin(HttpUser):
    host = host_url
    wait_time = between(1, 2)
    tasks = [TaskCase]
