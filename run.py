# coding=utf-8
import unittest
from common.handle_dir import CASE_DIR, REPORT_DIR

from unittestreport import TestRunner

suite = unittest.defaultTestLoader.discover(CASE_DIR, pattern="test*.py")
runner = TestRunner(suite, filename="report.html",
                    report_dir=REPORT_DIR,
                    title="测试报告", tester="Lyle",
                    desc="DREO接口自动化测试报告", templates=1)
runner.run()
