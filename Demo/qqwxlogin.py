# -*- coding: UTF-8 -*-
import pymysql
import itchat
import wxpy
from apscheduler.schedulers.blocking import BlockingScheduler
import time


class TtUitl:
    # 链接数据库,db是具体的数据库库名
    try:
        conn = pymysql.connect(host="172.16.51.32", port=3306, user="root", passwd="root", db="test",
                               charset='utf8')
        print("conn db success")
    except (AttributeError, pymysql.OperationalError):
        print("message : conn db error")

    # 获取操作游标
    def cursor(self):
        if self.conn is not None:
            # 获取操作游标
            return self.conn.cursor()
        else:
            print("db conn failed")

    # 关闭数据库链接
    def closeDB(self):
        if self.conn is not None:
            return self.conn.close()
        else:
            print("db conn failed")


def getIp():
    # 1.打开链接
    cursor = TtUitl().cursor()
    ips = []
    if cursor is not None:
        sql = "select sname from student"
        cursor.execute(sql)
        rows = cursor.fetchall()

        # 获取查询的返回值
        for row in rows:
            # 获取查询的返回值中某一个字段
            for i in range(0, len(row)):
                print(row[i])
                # 判断这个值是否已经存在了列表中，如果没有存在就加入，存在就忽略
                if row[i] not in ips:
                    ips.append(row[i])
                else:
                    print("这个ip已经操作过，忽略：" + row[i])

    TtUitl().closeDB()
    return ips


def sedWxMsg(msg):
    loginTag = loginWx()
    if loginTag == 1:
        friend = itchat.search_friends(name=u'Mango')
        if friend is not None:
            name = friend[0]["UserName"]
            itchat.send_msg(msg, toUserName=name)
            return 0
        else:
            print("get wechat friend failed")
            return -1
    else:
        print("wechat login failed")


def loginWx():
    # 微信网页登陆1 __没有成功
    # bot = wxpy.Bot(console_qr=2, cache_path='botoo.pkl')
    try:
        # 微信网页登陆2 __没有成功
        itchat.auto_login(hotReload=True)
        print("wechat login success...")
        return 0
    except():
        return -1


def testJob(msg):
    print(msg)

def job():
    scheduler = BlockingScheduler()
    scheduler.add_job(testJob("py test msg"), "cron", day_of_week="1-5", hour=16, minute=25)
    scheduler.start()


if __name__ == "__main__":
    names = []
    names = getIp()
    print(names)
    job()
