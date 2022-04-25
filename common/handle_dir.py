# coding=utf-8

"""
@author:lyle.hong
@date:2022/4/15 17:14
"""
import os

# 项目根路径
BASE_PATH = os.path.dirname(os.path.dirname(__file__))

# 数据路径
DATA_DIR = os.path.join(BASE_PATH, "datas")

# 报告路径
REPORT_DIR = os.path.join(BASE_PATH, "reports")

# 日志路径
LOG_DIR = os.path.join(BASE_PATH, "logs")

# 用例执行路径
CASE_DIR = os.path.join(BASE_PATH, "testcase")

# 配置文件路径
CONF_DIR = os.path.join(BASE_PATH, "conf")
