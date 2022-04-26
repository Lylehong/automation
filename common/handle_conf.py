# coding=utf-8

"""
@author:lyle.hong
@date:2022/4/19 12:09
"""
import os
from configparser import ConfigParser
from common.handle_dir import CONF_DIR

conf = ConfigParser()
fp = os.path.join(CONF_DIR, "conf.ini")
conf.read(fp)

