# coding=utf-8

"""
@author:Lyle.Hong
@date:2022/4/24 9:44
"""
import random
import time

from faker import Faker


class Fakers:
    """测试数据"""

    def __init__(self, locale):
        """
        :param locale: zh_CN：中国，en_US:美国
        """
        self.fk = Faker(locale=locale)

    def get_email(self):
        """
        获取ascii随机邮箱
        :return:
        """
        rd = "hesung.123"
        email = rd + self.fk.ascii_email()
        return email

    def get_nickname(self):
        """
        获取随机名称
        :return:
        """
        rd = "hesung.name"
        nickname = self.fk.name()
        return rd + nickname

    def get_first_name(self):
        """
        获取随机firstname
        :return:
        """
        rd = "hesung."
        first_name = self.fk.first_name()
        return rd + first_name

    def get_last_name(self):
        """
        获取随机lastname
        :return:
        """
        rd = "hesung."
        first_name = self.fk.last_name()
        return rd + first_name

    def get_romanized_name(self):
        """
        获取罗马名
        :return:
        """
        rd = "hesung."
        rm = self.fk.romanized_name().split()
        return rd + rm[0], rd + rm[1]

    def get_phone_number(self):
        """
        获取随机手机号
        :return:
        """
        rd = ["110", "120", "119"]
        num = str(self.fk.phone_number())[3:]
        return random.choice(rd) + num

    def get_street_address(self):
        """
        获取街道地址
        :return:
        """
        return self.fk.street_address()

    def get_street_name(self):
        """
        获取街道名称
        :return:
        """
        return self.fk.street_name()

    def get_city_name(self):
        """
        获取城市名称
        :return:
        """
        return self.fk.city()

    def get_country_name(self):
        """
        获取国家名称
        :return:
        """
        return self.fk.country()

if __name__ == '__main__':
    print(Fakers("zh_CN").get_phone_number())
