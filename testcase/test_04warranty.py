# coding=utf-8

"""
@author:Lyle.Hong
@date:2022/4/26 13:56
"""
import os
import random
import time

import requests

from common.handle_assert import assert_in_dict
from common.handle_data import replace_data
from common.handle_excel import HandleExcel
from common.handle_faker import get_romanized_name, get_phone_number
from common.handle_log import my_log
from utils.authorization import BaseCase
from unittestreport import ddt, list_data
from common.handle_dir import DATA_DIR
from common.handle_conf import conf


@ddt
class TestWarranty(BaseCase):
    """延保"""
    excel = HandleExcel(os.path.join(DATA_DIR, "延保接口用例.xlsx"), "延保")
    cases = excel.read_data()

    # base_url
    base_url = conf.get("request", "url")
    # headers
    headers = eval(conf.get("request", "headers"))

    @classmethod
    def setUpClass(cls) -> None:
        # 登录成功
        cls.login_authorization()
        # 添加请求头authorization
        cls.headers["Authorization"] = cls.Authorization

    @list_data(cases)
    def test_warranty(self, item):
        """
        延保接口
        :param item:
        :return:
        """
        # url
        url = self.base_url + item["url"]
        # method
        method = item["method"].lower()
        # title
        title = item["title"]
        # data
        data = item["data"]
        # 替换数据

        if title == "官网渠道-延保成功":
            TestWarranty.purchased_channel = "Dreo Official Website"
            TestWarranty.order_number = "DREO" + str(random.randint(1000, 9999))
        if title == "亚马逊渠道-延保成功":
            TestWarranty.purchased_channel = "Dreo Official Website"
            TestWarranty.order_number = "DREO" + str(random.randint(1000, 9999))

        TestWarranty.first_name, TestWarranty.last_name = get_romanized_name()
        TestWarranty.phone = "+1" + get_phone_number()
        TestWarranty.current_time = time.strftime("%Y/%m/%d", time.localtime())
        data = replace_data(data, TestWarranty)
        # expected
        expected = eval(item["expected"])
        # 请求
        response = requests.request(method=method, url=url, json=eval(data), headers=self.headers)
        resp = response.json()
        print(resp)
        try:
            if resp["code"] == 0 and resp["msg"] == "OK":
                # TODO:未完成
                # 校验用户名

                # 校验订单号

                # 校验手机号

                # 校验日期
                pass
            else:
                assert_in_dict(expected, resp)
        except AssertionError as e:
            my_log.error("--【{}】--用例执行失败".format(title))
            my_log.exception(e)
            raise e
        else:
            my_log.info("--【{}】--用例执行成功".format(title))
