# 第一种告警，有上线时间但是没有关联版本预警

import datetime
import json
import requests

from utils.mysql_DBUtils import MyPymysqlPool

test_url = 'https://open.feishu.cn/open-apis/bot/v2/hook/ceec3d80-fdf0-428d-b37b-6faa50ff3a8e'
yujing_url = 'https://open.feishu.cn/open-apis/bot/v2/hook/1d21cf5b-5cab-4eb6-8600-2ad028b07ba7'
feishu_url = test_url

def stroy_without_onlinetime():
    headers = {
        'Content-Type': 'application/json'
    }


    jira_mysql = MyPymysqlPool('jiraMysql')

    stroy_without_onlinetime_sql = "SELECT issue_key,summary FROM tech WHERE DATE_FORMAT(on_line_time,'%Y-%m-%d') = DATE_FORMAT(NOW(),'%Y-%m-%d') and project_key in ('NSP') AND fix_version = '' "

    stroy_without_onlinetime_result = jira_mysql.getAll(stroy_without_onlinetime_sql)

    print(stroy_without_onlinetime_result)

    # 释放数据库连接池
    jira_mysql.dispose()
    data = ''

    if stroy_without_onlinetime_result:

        for i in stroy_without_onlinetime_result:
            text = str(i) + "\n"
            data += text

        data_stroy_without_onlinetime = {
            "msg_type": "text",
            "content": {
                "msg": "业务平台预警:",
                "text": "有上线时间但是没有关联版本预警，" + "预计上线时间是：" + str(
                    datetime.datetime.strftime(datetime.datetime.today(),
                                               '%Y-%m-%d')) + "\n但是下面的需求没有关联版本，有延期风险：\n" + str(
                    data)
            }
        }

    else:
        data_stroy_without_onlinetime = {
            "msg_type": "text",
            "content": {
                "msg": "业务平台预警:",
                "text": "预计上线时间是：" + str(
                    datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')) + "\n当前没有未关联版本的需求，正常："
            }
        }

    req_data_stroy_without_onlinetime = requests.post(headers=headers, data=json.dumps(data_stroy_without_onlinetime),
                                                      url=feishu_url).json()
    print(req_data_stroy_without_onlinetime)


def submit_test_delay():
    headers = {
        'Content-Type': 'application/json'
    }


    jira_mysql = MyPymysqlPool('jiraMysql')
    submit_test_delay_sql = "SELECT s.issue_key,s.summary,s.`status` FROM story s WHERE DATE_FORMAT(s.plan_time,'%Y-%m-%d') = date_sub(curdate(),interval -1 day) and s.project_key in ('NSP') " \
                            "AND s.`status` in ('待办','需求设计中','需求设计完成','需求评审完成','开发中') " \
                            "UNION " \
                            "SELECT t.issue_key,t.summary,t.`status` FROM tech t WHERE DATE_FORMAT(t.plan_time,'%Y-%m-%d') = date_sub(curdate(),interval -1 day) and t.project_key in ('NSP') " \
                            "AND t.`status` in ('待办','开发中')"

    submit_test_delay_result = jira_mysql.getAll(submit_test_delay_sql)

    print(submit_test_delay_result)

    # 释放数据库连接池
    jira_mysql.dispose()
    data = ''

    if submit_test_delay_result:

        for i in submit_test_delay_result:
            text = str(i) + "\n"
            data += text

        submit_test_delay_data = {
            "msg_type": "text",
            "content": {
                "msg": "提测延期预警:",
                "text": "延期提测风险预警，" + "预计提测时间是：" + str(
                    datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=1),
                                               '%Y-%m-%d')) + "\n但是下面的需求还没进入提测状态，有延期风险：\n" + str(data)
            }
        }

    else:
        submit_test_delay_data = {
            "msg_type": "text",
            "content": {
                "msg": "提测延期预警:",
                "text": "预计提测时间是：" + str(
                    datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=1),
                                               '%Y-%m-%d')) + "\n明天没有需要提测需求，正常："
            }
        }

    submit_test_delay_req = requests.post(headers=headers, data=json.dumps(submit_test_delay_data),
                                                      url=feishu_url).json()
    print(submit_test_delay_req)


if __name__ == '__main__':
    stroy_without_onlinetime()
    submit_test_delay()
