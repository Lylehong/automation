# coding=utf-8

"""
@author:Lyle.Hong
@date:2022/4/26 15:06
"""
import yaml


class HandleYaml:
    """操作yaml数据"""

    def __init__(self, file_path):
        self.file_path = file_path

    def read_yaml(self):
        """
        读取yaml数据
        :return:
        """
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data

    def write_yaml(self, data):
        """
        写入yaml
        :param data:
        :return:
        """
        with open(self.file_path, "w") as f:
            yaml.dump(data, f, allow_unicode=True)


if __name__ == '__main__':
    a = HandleYaml(r"D:\automation\conf\login.yaml")
    print(a.read_yaml())