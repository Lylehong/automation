# coding=utf-8

"""
@author:lyle.hong
@date:2022/4/21 9:09
"""
import re


class TestMode:
    email = "alexhong@gmail.com"
    passwd = "hl19930321"


def replace_data(data, cls):
    """
    正则匹配替换Excel中的数据
    :param data: 匹配字符串
    :param cls: 类对象
    :return:
    """
    while re.search("#(.+?)#", data):
        res = re.search("#(.+?)#", data)
        item = res.group()
        attr = res.group(1)
        value = getattr(cls, attr)
        data = data.replace(item, str(value))
    return data


if __name__ == '__main__':
    data = '{"client_id":"6c2bfbdd497f4addbb77449edd3d73ec","client_secret": "460df321de794ea08110cb3ed32c7452","grant_type": "email-password","scope": "all","email": "#email#","password": "#passwd#","encrypt": "ciphertext","himei": "a3613f6f1e9cf62808e8d0eda0a6bc4c"}'
    print(replace_data(data, TestMode))
