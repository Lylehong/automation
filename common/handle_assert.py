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
                        act_list = act[k].split("|")
                        # 判断分割后所有数据是否在预期结果中
                        for li in act_list:
                            if li.strip() in expected[k]:
                                pass
                            else:
                                raise AssertionError("{} not in {}".format(li, act[k]))
                    else:
                        raise AssertionError("{} not equal {}".format(expected[k], act[k]))
                else:
                    raise AssertionError("{} not equal {}".format(expected[k], act[k]))
            else:
                assert_in_dict(expected[k], act[k])


if __name__ == '__main__':
    exp = {'code': 100008, 'msg': 'productCategory:product category is empty | country:country code invalid | country:country code is empty'}
    act = {'code': 100008, 'msg': 'productModel:product model is empty'}
    print(assert_in_dict(exp, act))
