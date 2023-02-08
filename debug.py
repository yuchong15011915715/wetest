# write you code

import requests
import datetime
import time

token = ''
# 测试环境配置
host_api_for_test = 'https://qa-a.szzhijing.com'
getgrantCode_url_for_test = 'https://qa-a.szzhijing.com/uac/iuauthen/passwordSignOnGrant'
clientId_for_test = '3FE92F32AF7B4ED7B2F9BC8CEB9023D3'
loginAccount_for_test = '13764757307'
loginPassword_for_test = '123456'

host_url = 'https://qa-a.szzhijing.com'
clientId = '50EECEB9F781417DA11B0D4EB55386D1'


def get_today():
    return time.strftime("%Y-%m-%d")


def get_special_date(off=0):
    # 获取相对于今天的指定日期
    return (datetime.now() + datetime.timedelta(off)).strftime('%Y-%m-%d')


def get_special_time(h, m, s, off=0):
    # 获取相对于今天的指定时间
    return (datetime(datetime.now().year, datetime.now().month, datetime.now().day, h, m, s) + datetime.timedelta(off)).strftime(
        '%Y-%m-%d %H:%M:%S')


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def get_timestamp():
    t = time.time()
    return int(t)


def sleep(t):
    time.sleep(t)


def get_b2b_order():
    index = 1
    total_money = 0
    total_num = 1
    while index <= int(total_num / 20) + 1:
        data = {
            "dealType": "1",
            "tagIds": [],
            "pageNum": index,
            "pageSize": 20
        }
        header = {
            "accessToken": "B26B49F6690B412F976BD1118A6B29F7",
            "authen-type": "V2",
            "clientId": 'D0481B38729C4454A4AAA128DBD50852',
            'userId': '7E1FEF617B8A4242AAEB1AFF95E1A83A'
        }
        req = requests.post("https://a.szzhijing.com/b2bmember/vipusercustomer/web/listPage", json=data,
                            headers=header)

        result = req.json()
        total_num = result['body']['total']
        print(str(total_num) + '; 当前的index:' + str(index))
        print(str(result['body']['list']))
        for i in range(len(result['body']['list'])):
            index_money = result['body']['list'][i]['dealDescribeDTO']['dealAmount']
            print(str(index_money))
            total_money = total_money + int(index_money)
        index += 1
        print("______________________")
        print(total_money)


if __name__ == '__main__':
    index = 1


    # 获取今天（现在时间）
    today = datetime.datetime.today()
    to = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
    print(to)
    # 昨天
    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
    yd = datetime.datetime.strftime(yesterday, '%Y-%m-%d')
    print(yd)
    # 明天
    # tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    to = datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=1), '%Y-%m-%d')
    print(to)
