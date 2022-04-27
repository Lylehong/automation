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
                # 增加“|”左右两边随机变化判断
                elif isinstance(expected[k], str):
                    if "|" in expected[k] and "|" in act[k]:
                        act1, act2 = act[k].split("|")
                        new_act = "{} | {}".format(act2.strip(), act1.strip())
                        if expected[k] == new_act:
                            pass
                        else:
                            raise AssertionError("{} not equal {}".format(act1, act[k]))
                else:
                    raise AssertionError("{} not equal {}".format(expected[k], act[k]))
            else:
                assert_in_dict(expected[k], act[k])


if __name__ == '__main__':
    exp = {'code': 100008, 'msg': 'country:country code invalid | country:country code is empty'}
    act = {'code': 100008, 'msg': 'country:country code is empty | country:country code invalid'}
    print(assert_in_dict(exp, act))
