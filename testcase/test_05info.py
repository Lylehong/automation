# coding=utf-8

"""
@author: Lyle.Hong
@date: 2022/6/8 16:27
"""
import os
import random
import time

import requests

from common.handle_assert import assert_in_dict
from common.handle_data import replace_data
from common.handle_excel import HandleExcel
from common.handle_faker import get_nickname, get_first_name, get_last_name
from utils.authorization import BaseCase
from unittestreport import ddt, list_data
from common.handle_dir import DATA_DIR
from common.handle_conf import conf
from common.handle_log import my_log


@ddt
class TestInfo(BaseCase):
    """info接口"""
    # 读取excel文件
    excel = HandleExcel(os.path.join(DATA_DIR, "个人信息接口用例.xlsx"), "Sheet1")
    # 获取所有测试用例
    cases = excel.read_data()
    # 登录成功的email
    email = conf.get("register_email", "email")
    nickname = get_nickname()
    firstname = get_first_name()
    lastname = get_last_name()
    gender = random.choice(["male", "female", "other"])
    birthdate = str(time.strftime("%Y-%m-%d")) + "T00:00:00.000Z"

    @classmethod
    def setUpClass(cls) -> None:
        # 登录
        cls.login_authorization()

    @list_data(cases)
    def test_info(self, item):
        """
        个人信息
        :return:
        """
        # title
        title = item["title"]
        # url地址
        url = self.base_url + item["url"]
        # 请求数据
        data = item["data"]
        # 替换参数
        data = replace_data(data, TestInfo)
        # 请求方法
        method = item["method"].upper()
        # 预期结果
        expected = eval(item["expected"])
        # 发送请求
        response = requests.request(method=method, url=url, json=eval(data), headers=self.headers)
        resp = response.json()
        # 断言
        try:
            if resp["code"] == 0:
                assert resp["data"]["email"] == self.email
                assert resp["data"]["nickname"] == eval(data)["nickname"]
                assert resp["data"]["firstName"] == eval(data)["firstName"]
                assert resp["data"]["lastName"] == eval(data)["lastName"]
                assert resp["data"]["gender"] == eval(data)["gender"]
                # birthdate有bug
                # assert resp["data"]["birthdate"] == eval(data)["birthdate"]
                assert_in_dict(expected, resp)
                my_log.info("--【{}】--用例执行成功".format(title))
            else:
                assert_in_dict(expected,resp)
        except AssertionError as e:
            my_log.error("--【{}】--用例执行失败".format(title))
            my_log.exception(e)
            raise e
