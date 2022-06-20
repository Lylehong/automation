# coding=utf-8

"""
@author: Lyle.Hong
@date: 2022/6/6 9:01
"""
# 没有官网预发布账号密码，验证不了
import pymysql
from sshtunnel import SSHTunnelForwarder
host_jump = "10.10.20.96"
port_jump = ""
user_name_jump = "lyle.hong"
user_password = "hl19930321"
host_mysql = ""
port_mysql = ""

with SSHTunnelForwarder(
        (host_jump, int(port_jump)),  # 跳板机的配置
        # ssh_pkey=ssh_pk_jump,
        # 密钥的访问方式，如果是密码 ssh_password=？？？
        ssh_username=user_name_jump,
        ssh_password=user_password,
        remote_bind_address=(host_mysql, int(port_mysql))) as server:
    conn = pymysql.connect(host="127.0.0.1",port=server.local_bind_port,user="")
