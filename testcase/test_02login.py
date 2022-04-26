# coding=utf-8

"""
@author:lyle.hong
@date:2022/4/15 17:00
"""

import unittest
import requests
import os
from unittestreport import ddt, list_data
from common.handle_excel import HandleExcel
from common.handle_conf import conf
from common.handle_dir import DATA_DIR
from common.handle_assert import assert_in_dict
from common.handle_log import my_log
from utils.authorization import BaseCase


@ddt
class TestLogin(BaseCase):
    # 获取用例数据
    excel = HandleExcel(os.path.join(DATA_DIR, "登录接口用例.xlsx"), "Sheet1")
    cases = excel.read_data()
    # 获取请求头
    headers = eval(conf.get("request", "headers"))
    # 获取默认url根路径
    base_url = conf.get("request", "url")

    @list_data(cases)
    def test_login(self, itme):
        # 更新请求头部
        headers = self.headers
        # 获取请求url地址
        url = self.base_url + itme["url"]
        # 获取请求方法
        method = itme["method"].lower()
        # 获取请求参数
        data = eval(itme["data"])
        # 获取title
        title = itme["title"]
        # 获取预期结果
        expected = eval(itme["expected"])
        # 发送请求，获取实际结果
        resp = requests.request(method=method, url=url, json=data, headers=headers)
        res = resp.json()
        try:
            assert_in_dict(expected, res)
        except AssertionError as e:
            my_log.error("--【{}】--用例执行失败".format(title))
            my_log.exception(e)
            raise e
        else:
            my_log.info("--【{}】--用例执行成功".format(title))
