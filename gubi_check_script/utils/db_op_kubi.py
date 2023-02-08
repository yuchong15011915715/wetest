#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
数据库操作 封装类
create by zean.chen
2018.8.6

说明：
实现对测试数据库的插入、删除

python2依赖库：MySQLdb
下载whl文件：https://download.lfd.uci.edu/pythonlibs/l8ulg3xw/MySQL_python-1.2.5-cp27-none-win_amd64.whl
https://pypi.org/project/MySQL-python/#files
https://files.pythonhosted.org/packages/27/06/596ae3afeefc0cda5840036c42920222cb8136c101ec0f453f2e36df12a0/MySQL-python-1.2.5.win32-py2.7.exe
使用pip安装：pip install .\MySQL_python-1.2.5-cp27-none-win_amd64.whl

python3依赖库
pymysql：pip3 install PyMySQL
"""
import time

import pymysql


class DBOperate:
    def sql_select_course_info(self, start=0, limit=100):
        sql_str = """SELECT id, `code`, `name`, course_picture_url,standard_img_url, ai_course_url, 
            static_resource_url, media_resource_url, video_url FROM course LIMIT %d, %d""" % (start, limit)
        return self.sql_select_execute(sql_str)

    def sql_select(self, sql_expression):
        self._connect()
        try:
            self.cur.execute(sql_expression)
            result = self.cur.fetchall()
        except pymysql.Error as e:
            print("Mysql Error select from account")
            result = None
        self._disconnect()
        return result

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

    def sql_select_fetchone(self, sql_str):
        self._connect()
        try:
            self.cur.execute(sql_str)
            result = self.cur.fetchone()
        except pymysql.Error as e:
            print("Mysql Error select from account")
            result = None
        self._disconnect()
        return result

    def sql_insert_execute(self, sql_str):
        self._connect()
        try:
            self.cur.execute(sql_str)
            self.cur.execute("select LAST_INSERT_ID()")
            inserted_id = self.cur.fetchone()[0]
        except pymysql.Error as e:
            print("Mysql Error select from account")
            inserted_id = 0
        self._disconnect()
        return inserted_id

    def sql_update_execute(self, sql_str):
        self._connect()
        try:
            self.cur.execute(sql_str)
            print('sql update: ' + sql_str)
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
        self._disconnect()
        return

    def sql_execute(self, sql_expression):
        self._connect()
        try:
            # 执行sql语句
            self.cur.execute(sql_expression)
            # 提交到数据库执行
            self.conn.commit()
        except:
            # Rollback in case there is any error
            self.conn.rollback()

    def _connect(self):
        try_count = 0
        while try_count < 2:
            try_count = try_count + 1
            try:
                self.conn = pymysql.connect(
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
        #             time.sleep(1)
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))


if __name__ == "__main__":
    dbop = DBOperate()
    print(dbop.sql_select_fetchone("SELECT * FROM `reservoir_info`"))
