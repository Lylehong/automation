# coding=utf-8

"""
@author:Lyle.Hong
@date:2022/4/26 9:10
"""
import os

import requests

from common.handle_data import replace_data
from common.handle_excel import HandleExcel
from common.handle_faker import get_email
from utils.authorization import BaseCase
from common.handle_dir import DATA_DIR
from common.handle_conf import conf
from unittestreport import ddt, list_data
from common.handle_assert import assert_in_dict
from common.handle_log import my_log


@ddt
class TestSubscribe(BaseCase):
    """订阅"""

    # 获取所有cases用例
    excel = HandleExcel(os.path.join(DATA_DIR, "订阅接口用例.xlsx"), "订阅")
    cases = excel.read_data()

    # 获取已注册成功邮箱
    email = conf.get("register_email", "email")
    # 获取headers
    headers = eval(conf.get("request", "headers"))
    # 获取url
    base_url = conf.get("request", "url")

    @list_data(cases)
    def test_subscribe(self, item):
        """
        订阅功能
        :return:
        """
        # 替换url参数
        current_url = replace_data(item["url"], TestSubscribe)
        url = self.base_url + current_url
        # 请求方法
        method = item["method"].lower()
        # 获取title
        title = item["title"]
        # 预期结果
        expected = eval(item["expected"])
        # 发送请求
        response = requests.request(method=method, url=url, headers=self.headers)
        res = response.json()
        try:
            # 断言
            if res["code"] == 0:
                assert_in_dict(expected, res)
                assert res["data"]["email"] == self.email
                assert res["data"]["id"] is not None
            elif res["code"] == 3050003 and res["msg"] == "You have subscribed.":
                # 获取随机邮箱发送订阅请求
                email = get_email()
                # 动态创建元类
                test_mode = type("TestMode", (object,), {"email": email})
                current_url = replace_data(item["url"], test_mode)
                url = self.base_url + current_url
                response = requests.request(method=method, url=url, headers=self.headers)
                res = response.json()
                assert_in_dict(expected, res)
                assert res["data"]["email"] == test_mode.email
                assert res["data"]["id"] is not None
            else:
                assert_in_dict(expected, res)
        except Exception as e:
            my_log.info("--【{}】--用例执行失败".format(title))
            raise e
        else:
            my_log.info("--【{}】--用例执行成功".format(title))
