# coding=utf-8

"""
@author:lyle.hong
@date:2022/4/15 18:22
"""
import pymysql
from common.handle_conf import conf


class HandleMySql:
    """封装mysql方法"""
    host = conf.get("mysql", "host")
    db = conf.get("mysql", "db")
    user = conf.get("mysql", "user")
    passwd = conf.get("mysql", "passwd")
    port = conf.getint("mysql", "port")

    def __init__(self):
        try:
            self.conf = pymysql.connect(host=self.host, db=self.db, user=self.user, passwd=self.passwd, port=self.port,
                                        cursorclass=pymysql.cursors.DictCursor,
                                        charset="utf8")
        except Exception as e:
            raise Exception("数据库连接错误 ==> {}".format(e))

    def execute_sql(self, sql):
        """
        执行sql 增删改
        :param sql:
        :return:
        """
        cur = self.conf.cursor()
        try:
            cur.execute(sql)
            self.conf.commit()
        except Exception as e:
            self.conf.rollback()
            raise Exception("SQL执行异常 ==> {}".format(e))
        return cur

    def search_one(self, sql):
        """
        查询一条数据
        :param sql:
        :return:
        """
        try:
            cur = self.execute_sql(sql)
            data = cur.fetchone()
        except Exception as e:
            raise Exception("查询数据错误 ==> {}".format(e))
        return data

    def search_all(self, sql):
        """
        查询所有数据
        :param sql:
        :return:
        """
        try:
            cur = self.execute_sql(sql)
            data = cur.fetchall()
        except Exception as e:
            raise Exception("查询数据错误 ==> {}".format(e))

        return data


if __name__ == '__main__':
    a = HandleMySql()
    res = a.search_one("select * from t_user;")
    print(res)
