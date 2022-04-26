# coding=utf-8

"""
@author:Lyle.Hong
@date:2022/4/22 10:00
"""
import os
import time

import requests

from common.handle_conf import conf, fp
from common.handle_dir import CONF_DIR
import unittest


class BaseCase(unittest.TestCase):
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

    @classmethod
    def login_authorization(cls):
        """
        登录账号成功
        :return:
        """
        # 读取email，passwd
        email = conf.get("register_email", "email")
        passwd = conf.get("register_email", "passwd")
        headers = eval(conf.get("request", "headers"))
        base_url = conf.get("request", "url")
        url = base_url + "/api/oauth/login?timestamp=1650419033518&lang=en-US"
        data = {"client_id": "6c2bfbdd497f4addbb77449edd3d73ec", "client_secret": "460df321de794ea08110cb3ed32c7452",
                "grant_type": "email-password", "scope": "all", "email": email,
                "password": passwd, "encrypt": "ciphertext",
                "himei": "a3613f6f1e9cf62808e8d0eda0a6bc4c"}
        response = requests.post(headers=headers, json=data, url=url)
        resp = response.json()
        # 保存
        try:
            if resp["msg"] == "OK" and resp["code"] == 0:
                # 保存类属性
                cls.Authorization = str(resp["data"]["token_type"]).capitalize() + " " + resp["data"]["access_token"]
            else:
                raise Exception("获取Authorization失败")
        except AssertionError as e:
            raise "请求Authorization失败:{}".format(e)

        # 写入文件
        # if resp["msg"] == "OK" and resp["code"] == 0:
        #     Authorization = str(resp["data"]["token_type"]).capitalize() + " " + resp["data"]["access_token"]
        #     # 写入配置文件
        #     conf.set("Authorization", "Authorization", Authorization)
        #     with open(fp, "w") as f:
        #         conf.write(f)
        # else:
        #     raise Exception("获取Authorization失败")
