#!/usr/local/bin/python3
# coding:utf-8
# 作者:浮尘
"""
在CMD命令行里输入"python xxx.py"来执行文件 这里主要讲下第一种方法：
左键双击运行脚本后，你会看到一个“闪退”的CMD窗口（“闪退”很快，从窗口弹出到消失只有0.1-0.2秒的时间，肉眼刚刚能看到），
根本看不到运行脚本后的结果，这是因为程序执行完后自动退出了，要让窗口停留，可以在代码最后放一个raw_input()。
关于Python和Paramiko在Windows里的安装，以及代码的执行就讲到这里，
下面进入第一个案例：
 案例1 案例背景：
 某公司有48口的思科3750交换机共1000台，分别分布在5个掩码为/24的B类网络子网下：
  172.16.0.x /24 172.16.1.x /24 172.16.2.x /24 172.16.3.x /24 172.16.4.x /24
案例需求： 在不借助任何NMS软件或网络安全工具的帮助的前提下，使用Python脚本依次ping所有交换机的管理IP地址，
来确定当前有哪些交换机可达，并且统计当前每个交换机有多少终端物理端口是UP的（级联端口不算），
以及1000台交换机所有UP的终端端物理端口的总数，并统计网络里的端口使用率(也就是端口的up率）。
案例思路： 根据需求我们可以写两个脚本，第一个脚本用来ping5个网段下所有交换机的管理IP，
因为掩码是/24，IP地址的最后一位我们可以指定python来ping .1到.254，
然后将所有可达的交换机IP写入并保存在一个名为reachable_ip.txt的文本文件中。
 之后，写第二个脚本来读取该文本文件中所保存的IP地址，依次登录所有这些可达的交换机，
 输入命令show ip int brief | i up命令查看有哪些端口是up的，再配合re这个模块(正则表达式），
 来匹配我们所要的用户端物理端口号(Gix/x/x)，统计它们的总数，即可得到当前一个交换机有多少物理端口是up的。
 （注：因为show ip int brief | i up的结果里也会出现10G的级联端口Tex/x/x以及虚拟端口，比如vlan或者loopback端口，
 所以这里强调的是用正则表达式来匹配用户端物理端口Gix/x/x）
"""
from datetime import datetime
import paramiko
import time
import re
import socket

now = datetime.now()
date = "%s-%s-%s" % (now.year, now.month, now.day)
time_now = "%s:%s:%s" % (now.hour, now.minute, now.second)


class Port_statistics(object):
    switch_with_tacace_issues = []
    switch_not_reachabled = []
    total_number_of_up_port = 0

    def __init__(self):
        self.ssh_login()
        self.summary()

    def ssh_login(self):
        self.iplist = open('reachable_ip.txt')
        self.number_of_switch = len(self.iplist.readlines())
        # print(self.number_of_switch)
        self.iplist.seek(0)
        for line in self.iplist.readlines():
            try:
                self.ip = line.strip()
                self.ssh_client = paramiko.SSHClient()
                self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh_client.connect(hostname=self.ip, username='ruijie', password='hipachuawei057!',
                                        look_for_keys=False)
                print("\nYou have successfully connected to", self.ip)
                self.command = self.ssh_client.invoke_shell()
                self.command.send('terminal length 0\n')
                self.check_up_port()
            except paramiko.ssh_exception.AuthenticationException:
                print("\nTACACS is not working for" + self.ip + ".")
                self.switch_with_tacace_issues.append(self.ip)
            except socket.error:
                print(self.ip + "is not reachable.")
                self.switch_not_reachabled.append(self.ip)
                self.iplist.close()

    def check_up_port(self):
        # self.command.send("term len 0\n")
        self.command.send("show int usage up \n")
        time.sleep(2)
        output = self.command.recv(65535).decode('ascii')
        print(output)
        self.ssh_client.close()
        self.search_up_port = re.findall(r'TenGigabitEthernet', output)
        self.number_of_up_port = len(self.search_up_port)
        # print(self.search_up_port)
        print(self.ip + "has" + str(self.number_of_up_port) + " ports up.")
        self.total_number_of_up_port += self.number_of_up_port
        # print(self.total_number_of_up_port)

    def summary(self):
        self.total_number_of_ports = self.number_of_switch * 48
        print("\n ")
        print("There are totally " + str(self.total_number_of_ports) + " ports available in the network.")
        print(str(self.total_number_of_up_port) + " ports are currently up.")
        print("Port up rate is %.2f%%" % (self.total_number_of_up_port / float(self.total_number_of_ports) * 100))
        print('\nTACACS is not working for below switches: ')

        for i in self.switch_with_tacace_issues:
            print(i)
            print("\nBelow switches are not reachable: ")
        for i in self.switch_not_reachabled:
            print(i)
            f = open(date + ".txt", "a+")
            f.write('As of ' + time_now + '\n')
            f.write("There are totally " + str(self.total_number_of_ports) + " ports available in the network.")
            f.write(str(self.total_number_of_up_port) + "ports are currently up.\n")
            f.write("Port up rate is %.2f%%" % (self.total_number_of_up_port / float(self.total_number_of_ports) * 100))
            f.write("\n"+('='*80)+"\n\n")
            f.close()


if __name__ == '__main__':
    Port_statistics()
