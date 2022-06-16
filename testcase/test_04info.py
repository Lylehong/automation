# coding=utf-8

"""
@author: Lyle.Hong
@date: 2022/6/8 16:27
"""
import os

import requests

from common.handle_assert import assert_in_dict
from common.handle_data import replace_data
from common.handle_excel import HandleExcel
from common.handle_faker import get_nickname
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
    # 获取请求头
    headers = eval(conf.get("request", "headers"))
    # 获取环境地址
    base_url = conf.get("request", "url")
    # 登录成功的email
    email = conf.get("register_email", "email")
    nickname = get_nickname()

    @classmethod
    def setUpClass(cls) -> None:
        # 登录
        cls.login_authorization()
        cls.headers["Authorization"] = cls.Authorization

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
        print(resp)
        # 断言
        try:
            assert resp["data"]["email"] == self.email
            assert_in_dict(expected, resp)
            my_log.info("--【{}】--用例执行成功".format(title))
        except AssertionError as e:
            my_log.error("--【{}】--用例执行失败".format(title))
            my_log.exception(e)
            raise e
