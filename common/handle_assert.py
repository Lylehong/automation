# coding=utf-8

"""
@author:lyle.hong
@date:2022/4/20 10:24
"""
from common.handle_log import my_log


def assert_in_dict(expected, act):
    """
    判断字典expected是否在字典act中存在
    :param expected:
    :param act:
    :return:
    """
    if not isinstance(expected, dict):
        raise TypeError("{} must be dict".format(expected))
    if not isinstance(act, dict):
        raise TypeError("{} must be dict".format(act))
    if expected and act:
        for k, v in expected.items():
            if not isinstance(v, dict):
                if expected[k] == act[k]:
                    pass
                else:
                    raise AssertionError("{} not equal {}".format(expected[k], act[k]))
            else:
                assert_in_dict(expected[k], act[k])
