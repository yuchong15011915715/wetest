import time
from random import randint
from locust import HttpUser, between, SequentialTaskSet, task
from zj_task.zjtest_utils import check, b2b_get_access_token

host_url = 'https://qa-a.szzhijing.com'
clientId = 'B612A51C00445E48ACD2225B1BD1831'

is_check = True
login_info = {"b2b_access_token": "", "user_id": ""}


# SequentialTaskSet 顺序执行task
class TaskCase(SequentialTaskSet):

    # 每个虚拟用户执行一次
    def on_start(self):
        b2b_user = [{"username": "15011915715", "password": "123456"},
                    {"username": "13800000001", "password": "123456"},
                    {"username": "15011910000", "password": "Aa123456"},
                    {"username": "15011910001", "password": "Aa123456"},
                    {"username": "15011910002", "password": "Aa123456"},
                    {"username": "15011910003", "password": "Aa123456"},
                    {"username": "15011910004", "password": "Aa123456"},
                    {"username": "15011910005", "password": "Aa123456"},
                    {"username": "15011910006", "password": "Aa123456"},
                    {"username": "15011910007", "password": "Aa123456"},
                    {"username": "15011910008", "password": "Aa123456"},
                    {"username": "15011910009", "password": "Aa123456"},
                    {"username": "15011910010", "password": "Aa123456"},
                    {"username": "15011910011", "password": "Aa123456"},
                    {"username": "15011910012", "password": "Aa123456"},
                    {"username": "15011910013", "password": "Aa123456"}]
        ranIndex = randint(0, len(b2b_user) - 1)
        username = b2b_user[ranIndex]["username"]
        # r"QWExMjM0NTY="
        password = b2b_user[ranIndex]["password"]
        print("————ranIndex：" + str(ranIndex) + ";取出来的用户信息：" + username + "," + password)
        b2b_get_access_token_req = b2b_get_access_token(username, r"QWExMjM0NTY=").split(',')
        b2b_access_token = b2b_get_access_token_req[0]
        user_id = b2b_get_access_token_req[0]
        login_info["b2b_access_token"] = b2b_access_token
        login_info["user_id"] = user_id

    # 获取抽奖信息
    @task(1)
    def get_lotteryInfo(self):
        # print("——on_start——里面的：" + login_info["b2b_access_token"])
        header = {
            "accessToken": login_info["b2b_access_token"]
        }
        params = {
            "activityId": "",
            "enterPriseId": "1455843005603778562"
        }
        with self.client.get("/b2bmarketing/activityLottery/getLotteryInfo", params=params, headers=header) as req:
            check(req, is_check, "get_lotteryInfo")

    # 获取助力数据
    @task(1)
    def get_attend_peopleInfo(self):
        url = "/b2bmarketing/specialActivity/getAttendPeopleInfo"
        data = {
            "publishUserId": "B62ADF9243E44C7597E31AFB94198C1F",
            "specialActivityId": "1"
        }
        with self.client.post(url, json=data) as req:
            check(req, is_check, "get_attend_peopleInfo")

    # 获取个人助力信息
    @task(1)
    def get_helpInfo(self):
        url = "/b2bmarketing/specialActivityUserPublish/findUserPublishActivity"
        params = {
            "specialActivityId": "1",
            "publishUserId": "B62ADF9243E44C7597E31AFB94198C1F"
        }
        with self.client.get(url, params=params) as req:
            check(req, is_check, "get_helpInfo")

    # 助力一次
    @task(1)
    def do_help(self):
        headers = {"Accept": "application/json, text/plain",
                   "Content-Type": "application/json",
                   "authen-type": "V2",
                   "clientId": "A102A3CE75B74258BDF7EB29FBEB8784",
                   "channelPlatform": "yousha"}
        params = {
            "specialActivityId": "1",
            "publishUserId": "446F7F89FDF1475A98BC89EB79B8FE3A",
            "unionId": "unionId" + str(int(time.time())),
            "openId": "openId" + str(int(time.time())),
            "headImgUrl": "https://thirdwx.qlogo.cn/mmopen/vi_32/k6jmx2BcrOkg5gZic0t3yTOOhicAmZdxsVicQIc4dF7BF5wwHAu8iclodKeBGMxv2zSs8DZsteYEnFtAnyyQ9lYfKA/132",
            "nickName": "冲@#.. " + str(int(time.time()))
        }
        url = "/b2bmarketing/specialActivityUserAttend/saveOrUpdate"
        with self.client.post(url, json=params, headers=headers) as req:
            check(req, is_check, "do_help")


class B2BLogin(HttpUser):
    host = host_url
    wait_time = between(1, 2)
    tasks = [TaskCase]


"""
if __name__ == "__main__":
    import os

    print("s执行性能测试")
    # 执行性能测试
    os.system("locust -f 有纱B2B.py --web-host=127.0.0.1")
"""
