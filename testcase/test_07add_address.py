# coding=utf-8

"""
@author: Lyle.Hong
@date: 2022/6/20 10:44
"""
from common.handle_assert import assert_in_dict
from common.handle_excel import HandleExcel
from common.handle_faker import Fakers
from common.handle_log import my_log
from utils.authorization import BaseCase
from unittestreport import ddt, list_data
from common.handle_data import replace_data


@ddt
class TestAddAddress(BaseCase):
    """新增收货地址"""
    # 获取测试用例数据
    excel = HandleExcel("新增收货地址接口用例.xlsx", "收货地址")
    cases = excel.read_data()
    # 准备测试数据
    fk = Fakers("en_US")
    firstName = fk.get_first_name()
    lastName = fk.get_last_name()
    phone = "+" + str(fk.get_phone_number())
    address1 = fk.get_street_name()
    address2 = fk.get_street_address()
    city = fk.get_city_name()
    country = fk.get_country_name()
    province = "New York"
    zip = 10002
    isDefault = True
    provinceCode = "NY"
    countryCode = "US"

    @classmethod
    def setUpClass(cls) -> None:
        cls.login_authorization()

    @list_data(cases)
    def test_add_address(self, item):
        """
        收货地址接口：/api/transaction/customer/address
        :return:
        """
        # url
        url = self.base_url + item["url"]
        # data
        data = item["data"]
        # 替换数据
        data = replace_data(data, TestAddAddress)
        # title
        title = item["title"]
        # expected
        expected = eval(item["expected"])
        response = self.rq(url=url, headers=self.headers, json=eval(data))
        try:
            # assert_in_dict(expected, response)
            if response["code"] == 0 and response["msg"] == "OK":
                assert response["data"]["address1"] == self.address1
                assert response["data"]["address2"] == self.address2
                assert response["data"]["city"] == self.city
                assert response["data"]["country"] == self.country
                assert response["data"]["countryCode"] == self.countryCode
                assert response["data"]["firstName"] == self.firstName
                assert response["data"]["lastName"] == self.lastName
                assert response["data"]["isDefault"] == self.isDefault
                assert response["data"]["phone"] == self.phone
                assert response["data"]["province"] == self.province
                assert response["data"]["provinceCode"] == self.provinceCode
                assert response["data"]["zip"] == str(self.zip)
                my_log.info("--【】--用例执行成功".format(title))
            else:
                assert_in_dict(expected, response)
                my_log.info("--【】--用例执行成功".format(title))
        except AssertionError as e:
            my_log.error("--【{}】--用例执行失败".format(title))
            my_log.exception(e)
            raise e
