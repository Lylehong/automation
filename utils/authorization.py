# coding=utf-8

"""
@author:Lyle.Hong
@date:2022/4/22 10:00
"""
import os
import time

import requests

from common.handle_conf import conf
from common.handle_dir import CONF_DIR


class BaseCase:
    """保存为类属性"""

    @classmethod
    def get_authorization(cls):
        """
        获取Authorization
        :return:
        """
        # 获取请求头
        headers = conf.get("request", "headers")
        # 获取url
        base_url = conf.get("request", "url")
        url = "/api/oauth/login?timestamp={}&lang=en-US".format(time.time())
        current_url = base_url + url
        # 请求参数
        data = {
            "client_id": "6c2bfbdd497f4addbb77449edd3d73ec",
            "client_secret": "460df321de794ea08110cb3ed32c7452",
            "grant_type": "client_credentials",
            "scope": "all"
        }
        # 发送请求
        response = requests.request(method="POST", url=current_url, json=data, headers=eval(headers))
        res = response.json()
        # 断言请求是否成功
        try:
            if res["msg"] == "OK" and res["code"] == 0:
                # 保存类属性
                cls.Authorization = str(res["data"]["token_type"]).capitalize() + " " + res["data"]["access_token"]
            else:
                raise Exception("获取Authorization失败")
        except AssertionError as e:
            raise "请求Authorization失败:{}".format(e)
