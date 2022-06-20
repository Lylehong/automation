# coding=utf-8

"""
@author:lyle.hong
@date:2022/4/15 17:00
"""

import requests
from unittestreport import ddt, list_data
from common.handle_excel import HandleExcel
from common.handle_conf import conf, fp
from common.handle_assert import assert_in_dict
from common.handle_log import my_log
from utils.authorization import BaseCase
from common.handle_faker import Fakers
from common.handle_data import replace_data


@ddt
class TestRegister(BaseCase):
    # 获取用例数据
    excel = HandleExcel("注册接口用例.xlsx", "注册")
    cases = excel.read_data()
    # 获取请求头
    headers = eval(conf.get("request", "headers"))
    # 获取默认url根路径
    base_url = conf.get("request", "url")
    fk = Fakers("zh_CN")

    def setUp(self) -> None:
        # 获取Authorization
        self.get_authorization()
        # 获取随机测试邮箱
        TestRegister.email = self.fk.get_email()
        # 获取随机名字
        TestRegister.nickname = self.fk.get_nickname()
        # 添加鉴权access_token
        self.headers["Authorization"] = self.Authorization

    def tearDown(self) -> None:
        # 更新access_token
        pass

    @list_data(cases)
    def test_register(self, itme):
        # 获取请求url地址
        if not itme["url"]:
            return
        url = self.base_url + itme["url"]
        # 获取请求方法
        method = itme["method"].upper()
        # 获取请求参数
        data = itme["data"]
        # 替换email
        data = replace_data(data, TestRegister)
        # 获取预期结果
        expected = eval(itme["expected"])
        # 获取title
        title = itme["title"]
        # 发送请求，获取实际结果
        resp = requests.request(method=method, url=url, json=eval(data), headers=self.headers)
        res = resp.json()
        try:
            if res["msg"] == "OK" and res["code"] == 0:
                assert_in_dict(expected, res)
                # 校验邮箱是否一致
                assert res["data"]["email"] == self.email
                # 校验nickname是否一致
                assert res["data"]["nickname"] == self.nickname
                # 校验id不为空
                assert res["data"]["id"] is not None
                # 保存邮箱至conf.ini
                conf.set("register_email", "email", self.email)
                with open(fp, "w") as f:
                    conf.write(f)
            elif title == "密码不符需求-字母+数字（小于8位）":
                msg = [
                    "password:Password min 8 characters, max 32 characters | password:Password at least one lowercase "
                    "letter and one number",
                    "password:Password at least one lowercase letter and one number | password:Password min 8 "
                    "characters, max 32 characters"]
                num = 0
                for exp in msg:
                    if exp == res["msg"]:
                        num += 1
                assert num == 1
            else:
                assert_in_dict(expected, res)

        except AssertionError as e:
            my_log.error("--【{}】--用例执行失败：".format(title))
            my_log.exception(e)
            raise Exception(e)
        else:
            my_log.info("--【{}】--用例执行成功".format(title))
