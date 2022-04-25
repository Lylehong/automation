# coding=utf-8

"""
@author:lyle.hong
@date:2022/4/19 9:41
"""
import logging
import os
import time
from common.handle_dir import LOG_DIR


class MyLogger:
    def __init__(self):
        # 创建日志收集器对象logger
        self.logger = logging.getLogger("my_logger")
        # 设置日志等级
        self.logger.setLevel("DEBUG")

        # 创建日志输出渠道，设置等级
        sh = logging.StreamHandler()
        sh.setLevel("INFO")

        # 输出到文件，设置等级
        rq = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        log_name = rq + ".log"
        log_path = os.path.join(LOG_DIR, log_name)
        fh = logging.FileHandler(log_path, encoding="utf-8")
        fh.setLevel("INFO")

        # 指定日志输出格式
        formatter = logging.Formatter("[%(asctime)s][%(filename)s-->line:%(lineno)d][%(levelname)s] %(message)s")
        sh.setFormatter(formatter)
        fh.setFormatter(formatter)

        # 添加日志输出到日志收集器
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)


# 创建一个日志收集器对象
my_log = MyLogger().logger
