# coding=utf-8

"""
@author: Lyle.Hong
@date: 2022/5/17 18:19
"""
import os

from case.dreo_place_order import DreoPlaceOrder
from common.handle_conf import conf
from common.handle_excel import HandleExcel
from utils.authorization import BaseCase
from unittestreport import ddt, list_data
from common.handle_dir import DATA_DIR


class TestPlaceOrder(BaseCase):
    """登录-加入购物车-下单"""
    po = DreoPlaceOrder()
    # excel = HandleExcel(os.path.join(DATA_DIR, "下单流程接口用例.xlsx"), "Sheet1")
    # cases = excel.read_data()
    # url
    headers = eval(conf.get("request", "headers"))
    base_url = conf.get("request", "url")

    @classmethod
    def setUpClass(cls) -> None:
        # 登录成功
        cls.login_authorization()
        cls.headers["Authorization"] = cls.Authorization

    def test_dreo_place_order(self):
        """
        验证登录->下单流程
        :return:
        """
        email = conf.get("register_email", "email")
        # 激活账号
        resp = self.po.active_customer(self.headers, self.base_url, email)
        assert resp["msg"] == 'OK'
        # 获取亚马逊产品库存
        self.po.get_product(self.headers)
        # 获取购物车id
        self.po.get_customer_cart(self.headers, self.base_url)
        # 添加商品至购物车
        self.po.add_shopping_card(self.headers, self.base_url)
        # 添加地址
        self.po.add_address(self.headers, self.base_url)
        # 创建订单
        checkout_url = self.po.create_order(self.headers, email)
        # 刷新订单信息
        web_url = self.po.checkout_order(headers=self.headers, checkout_url=checkout_url)
        # webdriver付款
        self.po.payment_order(url=web_url)
        # 校验支付是否成功
        resp = self.po.self_order(self.base_url, self.headers)
        assert resp["code"] == 0
        assert resp["msg"] == "OK"
        assert len(resp["data"]["list"]) > 0
