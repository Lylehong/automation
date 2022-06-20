# coding=utf-8

"""
@author: Lyle.Hong
@date: 2022/6/17 11:44
"""
from case.dreo_case import TestDreoCase
from utils.authorization import BaseCase


class TestVerified(BaseCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.case = TestDreoCase()
        cls.case.login_authorization()

    def test_verified_by_code(self):
        # 发送验证码请求
        self.case.get_verify_code()

        # 获取验证码
        code = self.case.get_code_by_mysql()

        # 通过code码激活账号
        resp = self.case.verify(code)
        assert resp["code"] == 0
        assert resp["msg"] == "OK"
        assert resp["data"] is True
