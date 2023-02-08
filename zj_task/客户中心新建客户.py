import requests

from zj_task.zjtest_utils import uac_get_access_token, new_uac_get_access_token

clientId = 'FA98280021E64E8D9B8226E40E0151D7'
orgCode = 'DC796EF0402249AFB8FDE69627C7FA94'


def create_customer():
    # login_info = str(new_uac_get_access_token('15011915715', '123456')).split(",")
    # print("accessToken:" + login_info[0] + " | " + "userId：" + login_info[1])

    url = 'https://qa-a.szzhijing.com/plmz-osp-mdc/customer/saveOfUpdateCustomAndEnterpriseInfo';
    header = {
        "Content-Type": r"application/json",
        "authen-type": "V2",
        "clientId": clientId,
        "accessToken": "416252207FC5488A943F4B191BA170EB",
        "userId": "446F7F89FDF1475A98BC89EB79B8FE3A",
        "orgCode": orgCode
    }

    for i in range(1, 2):
        abbrZhName = '外企7'
        params = {
            "customerDTO": {
                "customerId": '',
                "orgCode": orgCode,
                "abbrZhName": abbrZhName,
                "abbrEnName": "",
                "customerCode": "",
                "customerStatus": "",
                "customerSource": "7",
                "opreateArea": "1",
                "customerType": "1",
                "craft": "",
                "materials": "",
                "productUse": "",
                "isForeignTrade": 0,
                "firstStageType": "",
                "customerTax": "",
                "customerGrade": "1",
                "remark": "伟大的备注",
                "businessProvinceCode": "150000000000",
                "businessProvince": "内蒙古自治区",
                "businessCityCode": "150100000000",
                "businessCity": "呼和浩特市",
                "businessAreaCode": "150104000000",
                "businessArea": "玉泉区"
            },
            'enterpriseInfoDTO': {
                "enterpriseInfoId": '',
                "natureEnterprise": "9",
                "fullName": abbrZhName,
                "fullNameEn": "",
                "enterpriseCode": "",
                "creditCode": "122345677766432",
                "registerLegalPerson": "",
                "registerLegalPhone": "",
                "registerLegalIdCard": "",
                "registeredAddress": "我顶我顶我顶我",
                "businessYear": "4",
                "registerCapital": "344",
                "isContrLegalPerson": "",
                "creditRisk": "",
                "taxClass": "1",
                "countryCode": "ABW",
                "country": "阿鲁巴岛",
                "provinceCode": "",
                "province": "",
                "cityCode": "",
                "city": "",
                "areaCode": "",
                "area": "",
                "townCode": "",
                "town": "",
                "registerArea": "1",
                "registerTime": "2022-02-26 00:00:00"
            }
        }
        req = requests.post(headers=header, json=params, url=url).json()
        print(req)
        # url_2 = 'https://qa-a.szzhijing.com/plmz-osp-mdc/customer/enterpriseCustomer/' + str(req['customerDTO']['customerId'])
        # req_2 = requests.get(url=url_2, headers=header).json()
        # print(req_2)


if __name__ == '__main__':
    create_customer()
