# coding:utf-8
import datetime
import time
"""
运行环境：python3
依赖库：requests, pymysql
pip3 install requests
pip3 install PyMySQL
"""
import requests
import pymysql


def do_request(method, url, retry_times=3, **kwargs):
    while 0 < retry_times:
        try:
            func = getattr(requests, method)
            resp = func(url, **kwargs)
            return resp
        except Exception as e:
            LogUtil.print_mjd("request error %s->%s:" % (method, url), e)
            retry_times -= 1
    return None


class DBOperate:
    def sql_select_course_info(self, start=0, limit=100):
        sql_str = """SELECT id, `code`, `name`, course_picture_url,standard_img_url, ai_course_url, 
            static_resource_url, media_resource_url, video_url FROM course LIMIT %d, %d""" % (start, limit)
        return self.sql_select_execute(sql_str)

    def sql_select_execute(self, sql_str):
        self._connect()
        try:
            self.cur.execute(sql_str)
            rows = self.cur.fetchall()
            columns = [col[0] for col in self.cur.description]
        except pymysql.Error as e:
            print("Mysql Error select from account")
            rows = []
            columns = []
        self._disconnect()
        return rows, columns

    def _connect(self):
        try_count = 0
        while try_count < 2:
            try_count = try_count + 1
            try:
                self.conn = pymysql.connect(
                    # todo: 在此处修改数据库环境
                    host='172.16.253.113',
                    port=3306,
                    user='root',
                    passwd='dbtest',
                    db='pjx',
                    charset='utf8'
                )
                # self.conn = sqlite3.connect('E:/workspace/11/db.sqlite3')
                self.cur = self.conn.cursor()
                break
            except pymysql.Error as e:
                time.sleep(0.5)
                print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def _disconnect(self):
        # 关闭数据库连接
        try:
            self.cur.close()
            self.conn.commit()
            self.conn.close()
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))


class LogUtil:
    def __init__(self):
        pass

    @staticmethod
    def print_mjd(log_text, *args):
        extent_item = " ".join([str(item) for item in args])
        print("**Course Check**", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "=>", log_text, extent_item)


class CourseCheck:
    def __init__(self):
        self.dbop = DBOperate()
        self.check_lines = 0
        self.errors = 0

    def check_course_info(self):
        check_result = []
        start = 0
        limit = 100
        while True:
            course_list, columns = self.dbop.sql_select_course_info(start, limit)
            if course_list is None or len(course_list) == 0:
                break
            start += limit
            cid = columns.index("id")
            name = columns.index("name")
            img1 = columns.index("course_picture_url")
            img2 = columns.index("standard_img_url")
            html = columns.index("ai_course_url")
            zip1 = columns.index("static_resource_url")
            zip2 = columns.index("media_resource_url")
            video = columns.index("video_url")
            for info in course_list:
                time.sleep(0.02)  # 增加延时，避免构成压力
                self.check_lines += 1
                self.assert_result(check_result, info[cid], info[name], columns[img1], self.check_img(info[img1]))
                self.assert_result(check_result, info[cid], info[name], columns[html], self.check_html(info[html]))
                self.assert_result(check_result, info[cid], info[name], columns[img2], self.check_img(info[img2]))
                self.assert_result(check_result, info[cid], info[name], columns[zip1], self.check_zip(info[zip1]))
                self.assert_result(check_result, info[cid], info[name], columns[zip2], self.check_zip(info[zip2]))
                self.assert_result(check_result, info[cid], info[name], columns[video], self.check_video(info[video]))
        self.logout_result(check_result)

    def check_img(self, _url):
        if _url is None or _url == "":
            return "no url"
        head = do_request("head", _url.strip())
        if head is None:
            return "超时或无法链接"
        if head.is_redirect:
            _url = head.headers["Location"]
            return self.check_img(_url.strip())
        else:
            if head.status_code != 200:
                return "status_code=%d 非200" % head.status_code
            if not head.headers['Content-Type'].startswith("image/"):
                return "Content-Type not image"
            if int(head.headers['Content-Length']) < 200:
                return "Content-Length too small"
            return "OK"

    def check_html(self, _url):
        if _url is None or _url == "":
            return "no url"
        head = do_request("head", _url.strip())
        if head is None:
            return "超时或无法链接"
        if head.is_redirect:
            _url = head.headers["Location"]
            return self.check_html(_url.strip())
        else:
            resp = do_request("get", _url)
            if resp.status_code != 200:
                return "status_code=%d 非200" % head.status_code
            if len(resp.text) < 200:
                return "Content-Length too small"
            if resp.text.find("<title>") < 0:  # 检查是否包含固定内容
                return "html content not correct"
            return "OK"

    def check_zip(self, _url):
        if _url is None or _url == "":
            return "OK"
        head = do_request("head", _url.strip())
        if head is None:
            return "超时或无法链接"
        if head.is_redirect:
            _url = head.headers["Location"]
            return self.check_zip(_url.strip())
        else:
            if head.status_code != 200:
                return "status_code=%d 非200" % head.status_code
            if head.headers['Content-Type'] != 'application/zip':
                return "Content-Type not zip"
            if int(head.headers['Content-Length']) < 200:
                return "Content-Length too small"
            return "OK"

    def check_video(self, _url):
        if _url is None or _url == "":
            return "OK"
        head = do_request("head", _url.strip())
        if head is None:
            return "超时或无法链接"
        if head.is_redirect:
            _url = head.headers["Location"]
            return self.check_video(_url.strip())
        else:
            if head.status_code != 200:
                return "status_code=%d 非200" % head.status_code
            if head.headers['Content-Type'] != 'video/mp4':
                return "Content-Type not video"
            if int(head.headers['Content-Length']) < 200:
                return "Content-Length too small"
            return "OK"

    def assert_result(self, result_list, course_id, course_name, check_item, check_result):
        print(course_id, course_name, check_item, check_result)
        if check_result != "OK":
            self.errors += 1
            result_list.append((course_id, course_name, check_item, check_result))

    def logout_result(self, result_list):
        print("测试完毕，共检查了%d行数据，错误项共%d个：" % (self.check_lines, self.errors))
        for items in result_list:
            print("id:%d, name:%s, 检查项目:%s, 错误内容:%s" % tuple(items))


if __name__ == '__main__':
    cc = CourseCheck()
    cc.check_course_info()
