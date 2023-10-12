#!/usr/local/bin/python3
# coding:utf-8
# 作者:浮尘
import paramiko
import time
import subprocess
import os
"""
查询管理网段设备ip地址，并将返回成功的ip保存到rechable.txt文件中，方便lab1遍历
"""

class Ping():
    third_octect = range(5)
    last_octet = range(1, 256)

    def __init__(self):
        self.ping()

    def ping(self):
        self.remove_last_reachable_ip_file_exist()
        for ip3 in self.third_octect:
            for ip4 in self.last_octet:
                self.ip = '10.250.' + str(ip3) + '.' + str(ip4)
                self.ping_result = subprocess.call(['ping', '-c', '2', self.ip])
                self.open_ip_record_file()
                self.check_ping_result()
                self.f.close()

    def open_ip_record_file(self):
        self.f = open('reachable_ip.txt', 'a')

    def check_ping_result(self):
        if self.ping_result == 0:
            self.f.write(self.ip + '\n')

    def remove_last_reachable_ip_file_exist(self):
        if os.path.exists('reachable_ip.txt'):
            os.remove('reachable_ip.txt')


if __name__ == '__main__':
    script1_1 = Ping()
