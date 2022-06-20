# coding=utf-8

"""
@author: Lyle.Hong
@date: 2022/6/17 14:21
"""
from common.handle_conf import conf
from common.handle_db import HandleMySql
from utils.authorization import BaseCase


class TestDreoCase(BaseCase):
    """官网流程"""
    db = HandleMySql()

    def register(self):
        pass

    def login(self):
        # 登录
        self.login_authorization()

    def get_verify_code(self):
        """
        调验证码接口
        :return:
        """
        # self.login_authorization()
        cur_url = "/api/user/register/email/verify"
        url = self.base_url + cur_url
        resp = self.rq(url, headers=self.headers, json={})
        assert resp["code"] == 0
        assert resp["msg"] == "OK"
        assert resp["data"] == True

    def get_code_by_mysql(self):
        """
        从数据库中读取code
        :return:
        """

        sql = "SELECT verifycode FROM `t_user_verify` v ,t_user t WHERE t.id = v.id and t.email = '{}'; ".format(
            self.email)
        verifycode = self.db.search_one(sql)
        return verifycode["verifycode"]

    def verify(self, code):
        """
        激活账号
        :return:
        """
        cur_url = "/api/user/register/email/verify/code"
        url = self.base_url + cur_url
        data = {
            "code": "{}".format(code)
                }
        return self.rq(url, headers=self.headers, json=data)

    def edit_info(self):
        pass

    def edit_password(self):
        pass


