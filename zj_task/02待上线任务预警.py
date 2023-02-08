# 代办需求飞书告警
# jira 数据库拉取
import datetime
import json
import requests

from utils.mysql_DBUtils import MyPymysqlPool


# 故事+技术需求  今天和明天要上线的汇总
def story_online():
    headers = {
        'Content-Type': 'application/json'
    }

    test_url = 'https://open.feishu.cn/open-apis/bot/v2/hook/ceec3d80-fdf0-428d-b37b-6faa50ff3a8e'
    feishu_url = 'https://open.feishu.cn/open-apis/bot/v2/hook/f9429099-8aa4-41dc-a924-5b1372db2485'

    jira_mysql = MyPymysqlPool("jiraMysql")

    # 今天要上线的需求
    story_sql_today = "SELECT issue_key,summary,status FROM story WHERE  DATE_FORMAT(on_line_time,'%Y-%m-%d') = DATE_FORMAT(NOW(),'%Y-%m-%d') " \
                      "and project_key in ('NSP') AND `status` in ('待办','需求设计中','需求设计完成','需求评审完成','开发中','提测','测试中') " \
                      " UNION " \
                      "SELECT issue_key,summary,status FROM tech WHERE  DATE_FORMAT(on_line_time,'%Y-%m-%d') = DATE_FORMAT(NOW(),'%Y-%m-%d') " \
                      "and project_key in ('NSP') AND `status` in ('待办','需求设计中','需求设计完成','需求评审完成','开发中','提测','测试中') "
    story_sql_today_result = jira_mysql.getMany(story_sql_today, 100)

    issue_num_today = ""
    if story_sql_today_result:
        for i in story_sql_today_result:
            data = str(i) + "\n"
            issue_num_today += data

        data_today = {
            "msg_type": "text",
            "content": {
                "msg": "业务平台告警通知",
                "text": str(
                    datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')) + "当前未完成测试上线的需求:\n" + str(
                    issue_num_today)
            }
        }

        req_today = requests.post(headers=headers, data=json.dumps(data_today), url=feishu_url).json()
        print(str(req_today))

    # 明天上线的需求
    story_sql_tomorrow = "SELECT issue_key,summary,status FROM story WHERE  DATE_FORMAT(on_line_time,'%Y-%m-%d') = date_sub(curdate(),interval -1 day) " \
                         "and project_key in ('NSP') AND `status` in ('待办','需求设计中','需求设计完成','需求评审完成','开发中','提测','测试中')" \
                         " UNION " \
                         "SELECT issue_key,summary,status FROM tech WHERE  DATE_FORMAT(on_line_time,'%Y-%m-%d') = date_sub(curdate(),interval -1 day) " \
                         "and project_key in ('NSP') AND `status` in ('待办','需求设计中','需求设计完成','需求评审完成','开发中','提测','测试中')"
    story_sql_tomorrow_result = jira_mysql.getAll(story_sql_tomorrow)
    issue_num_tomorrow = ""
    if story_sql_tomorrow_result:
        for i in story_sql_tomorrow_result:
            data_2 = str(i) + "\n"
            issue_num_tomorrow += data_2

    data_tomorrow = {
        "msg_type": "text",
        "content": {
            "msg": "业务平台告警通知",
            "text": str(datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=1),
                                                   '%Y-%m-%d')) + "要上线的需求:" + str(issue_num_tomorrow)
        }
    }

    req_tomorrow = requests.post(headers=headers, data=json.dumps(data_tomorrow), url=test_url).json()
    print(str(req_tomorrow))

    # 释放数据库连接资源
    jira_mysql.dispose()


if __name__ == '__main__':
    story_online()
