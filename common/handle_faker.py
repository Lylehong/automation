# coding=utf-8

"""
@author:Lyle.Hong
@date:2022/4/24 9:44
"""
import random
import time

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


def get_first_name():
    """
    获取随机firstname
    :return:
    """
    rd = "hesung."
    first_name = fk.first_name()
    return rd + first_name


def get_last_name():
    """
    获取随机lastname
    :return:
    """
    rd = "hesung."
    first_name = fk.last_name()
    return rd + first_name


def get_romanized_name():
    """
    获取罗马名
    :return:
    """
    rd = "hesung."
    rm = fk.romanized_name().split()
    return rd + rm[0], rd + rm[1]


def get_phone_number():
    """
    获取随机手机号
    :return:
    """
    rd = ["110", "120", "119"]
    num = str(fk.phone_number())[3:]
    return random.choice(rd) + num
