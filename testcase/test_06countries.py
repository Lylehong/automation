# coding=utf-8

"""
@author: Lyle.Hong
@date: 2022/6/20 10:22
"""
# 获取缓存地址（收货地址）
from case.dreo_case import TestDreoCase
from common.handle_log import my_log


class TestGetCountries(TestDreoCase):
    """收货地址页"""
    case = TestDreoCase()

    @classmethod
    def setUpClass(cls) -> None:
        cls.login_authorization()

    def test_get_countries(self):
        """
        获取所有收货地址
        :return:
        """
        response = self.case.get_all_countries()
        try:
            assert response["code"] == 0
            assert len(response["data"]) != 0
            my_log.info("--【{}】--用例执行成功".format("获取地址页"))
        except AssertionError as e:
            my_log.error("--【{}】--用例执行失败".format("获取地址页"))
            my_log.exception(e)
            raise e
