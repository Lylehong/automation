# coding=utf-8

"""
@author:Lyle.Hong
@date:2022/4/24 9:44
"""
from faker import Faker

fk = Faker(locale="zh_CN")


def get_email():
    """
    获取ascii随机邮箱
    :return:
    """
    rd = "hesung.123"
    email = rd + fk.ascii_email()
    return email


def get_nickname():
    """
    获取随机名称
    :return:
    """
    rd = "hesung.name"
    nickname = fk.name()
    return rd + nickname
