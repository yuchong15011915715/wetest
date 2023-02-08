import json

import requests

host_url = 'https://qa-a.szzhijing.com'
b2b_clientId = '5B612A51C00445E48ACD2225B1BD1831'

clientId = 'FA98280021E64E8D9B8226E40E0151D7'
orgCode = 'DC796EF0402249AFB8FDE69627C7FA94'


def check(response, is_check, method_name="默认方法"):
    if is_check:
        req_json = json.loads(str(response.text))
        print("【" + method_name + "】:" + str(req_json))
        try:
            if response.status_code == 200:
                if str(req_json["successful"]) == "True":
                    print(" successful !")
                elif str(req_json['successful']) == "False":
                    print("successful == False ,check failed !")
                else:
                    print("something is wrong !get response is wrong !!! ")
            else:
                print("failed request :  " + str(response.status_code))

        except Exception as e:
            response.failure(response.text + "--失败原因:json解析response失败--" + str(e))

    else:
        print("NO Check !!! ")


def b2b_get_access_token(loginAccount, loginPassword):
    url = "https://qa-a.szzhijing.com/b2bmember/security/app/v1/weblogin"
    data = {
        "clientId": b2b_clientId,
        "loginAccount": loginAccount,
        "loginPassword": loginPassword
    }

    header = {
        "accessToken": "0",
        "app_version": "2.9.8",
        "app_build": "20211025",
        "channel": "quanbu",
        "osVersion": "11",
        "clientId": b2b_clientId,
        "sys_code": "Android",
        "serviceVersion": "3.7.2",
        "userId": "0",
        "orgCode": "",
        "Accept": "application/json, text/plain, */*",
        "authen-type": "V2",
        "channelPlatform": "yousha",
        "enterpriseRecordId": "",
        "enterpriseName": "",
        "Content-Type": "application/json; charset=UTF-8"
    }

    req = requests.post(url=url, headers=header, json=data).json()
    if req["body"] is not None:
        if req["body"]["accessToken"] is not None:
            user_id = req["body"]["userId"]
            b2b_access_token = req["body"]["accessToken"]
            print(f"————b2b_access_token:" + b2b_access_token + ";  " + f"user_id:" + user_id + ";")
            return b2b_access_token + "," + user_id
    else:
        return print(f'获取accessToken失败')


def uac_get_access_token(loginAccount, loginPassword):
    # 获取grantCode 开始#
    url = 'https://qa-a.szzhijing.com/uac/iuauthen/passwordSignOnGrant'
    data = {
        "loginAccount": loginAccount,
        "clientId": ""
    }
    request_grant_token = requests.post(url=url, json=data).json()["result"]["grantCode"]
    # 获取grantCode 结束#
    print("————request_grant_token:" + str(request_grant_token))

    # 获取accessToken 开始#
    headers = {"Accept": r"application/json, text/plain, */*", "authen-type": "V2", "clientId": uac_clientId}
    login_url = host_url + "/common/userInfo/loginTWS"
    params = {
        "grantCode": request_grant_token,
        "loginPassword": loginPassword
    }
    result = requests.get(headers=headers, url=login_url, params=params).json()
    # 获取accessToken 结束#
    # print("————request_access_token:" + str(result))

    if result["result"]["accessToken"] is not None:
        user_id = result["result"]["userId"]
        uac_access_token = result["result"]["accessToken"]
        refresh_token = result["result"]["refreshToken"]
        print(f"————access_token:" + uac_access_token + ";  " + f"user_id:" + user_id + ";")
        return uac_access_token + "," + user_id

    else:
        return print(f'获取accessToken失败')


def new_uac_get_access_token_uat(loginAccount, loginPassword):
    # 获取grantCode 开始#
    url = 'https://uat-a.szzhijing.com/uac/iuauthen/passwordSignOnGrant'
    data = {
        "loginAccount": loginAccount,
        "clientId": clientId
    }
    head = {
        'Accept': r"application/json, text/plain, */*",
        "authen-type": "V2",
        'clientId': clientId,
        'orgCode': orgCode
    }
    request_grant_token = requests.post(url=url, json=data, headers=head).json()["result"]["grantCode"]
    # 获取grantCode 结束#
    print("————request_grant_token:" + str(request_grant_token))

    # 获取accessToken 开始#
    headers = {
        "Accept": r"application/json, text/plain, */*",
        "authen-type": "V2",
        "clientId": clientId,
        'orgCode': orgCode
    }
    login_url = 'https://uat-a.szzhijing.com/uac/authen/getAccessTokenByPassword'
    data = {
        "grantCode": request_grant_token,
        "password": loginPassword,
        "clientId": clientId
    }
    result = requests.post(headers=headers, url=login_url, json=data).json()
    # 获取accessToken 结束#
    # print("————request_access_token:" + str(result))

    if result["result"]["accessToken"] is not None:
        user_id = result["result"]["userId"]
        uac_access_token = result["result"]["accessToken"]
        refresh_token = result["result"]["refreshToken"]
        print(f"————access_token:" + uac_access_token + ";  " + f"user_id:" + user_id + ";")
        return uac_access_token + "," + user_id

    else:
        return print(f'获取accessToken失败')


def new_uac_get_access_token_qa(loginAccount, loginPassword):
    # 获取grantCode 开始#
    url = 'https://qa-a.szzhijing.com/uac/iuauthen/passwordSignOnGrant'
    data = {
        "loginAccount": loginAccount,
        "clientId": clientId
    }
    head = {
        'Accept': r"application/json, text/plain, */*",
        "authen-type": "V2",
        'clientId': clientId,
        'orgCode': orgCode
    }
    request_grant_token = requests.post(url=url, json=data, headers=head).json()["result"]["grantCode"]
    # 获取grantCode 结束#
    print("————request_grant_token:" + str(request_grant_token))

    # 获取accessToken 开始#
    headers = {
        "Accept": r"application/json, text/plain, */*",
        "authen-type": "V2",
        "clientId": clientId,
        'orgCode': orgCode
    }
    login_url = 'https://qa-a.szzhijing.com/uac/authen/getAccessTokenByPassword'
    data = {
        "grantCode": request_grant_token,
        "password": loginPassword,
        "clientId": clientId
    }
    result = requests.post(headers=headers, url=login_url, json=data).json()
    # 获取accessToken 结束#
    # print("————request_access_token:" + str(result))

    if result["result"]["accessToken"] is not None:
        user_id = result["result"]["userId"]
        uac_access_token = result["result"]["accessToken"]
        refresh_token = result["result"]["refreshToken"]
        print(f"————access_token:" + uac_access_token + ";  " + f"user_id:" + user_id + ";")
        return uac_access_token + "," + user_id

    else:
        return print(f'获取accessToken失败')