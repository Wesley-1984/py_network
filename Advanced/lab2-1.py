import time
import paramiko
import getpass
import sys
import re
import socket

username = 'ruijie'
password = 'hipachuawei057!'
iplist = open('reachable_ip.txt', 'r+')

switch_upgrade = []
switch_not_upgraded = []
switch_with_tacacs_issue = []
switch_not_rechable = []
with open('reachable_ip.txt','r+') as f:
    for line in iplist.readlines():
        try:
            ip_address = line.strip()
            # 创建SSH客户端对象
            ssh_client = paramiko.SSHClient()
            # 设置客户端的主机密钥策略为自动添加策略
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接到远程SSH服务器，首次连接时会自动添加未知主机的密钥
            ssh_client.connect(hostname=ip_address, username=username, password=password, look_for_keys=False)
            print("Successfully connected to", ip_address)
            # 创建Shell会话
            command = ssh_client.invoke_shell()
            command.send('terminal length 0\n')
            command.send('show ver\n')
            time.sleep(1)
            # 从远程服务器接收命令输出，解码字符ascii
            output = command.recv(65535).decode('ascii')
            command.send('wr m\n')
            #通过正则表达式re.search匹配output内容
            switch_model = re.search(r'S5750\w?-\w{8,10}-H', output)
            print(switch_model.group(0))
            software_version = re.search(r'S5700\w?_\w{4}\s(\S+)', output)
            # print(software_version)
            print(software_version.group(0))
            # sn = re.search(r'G1MWB8V\w{6}', output)
            #通过正则表达式re.findall匹配output中所有以'G1MWB8V'开始的内容
            sn = re.findall(r'G1MWB8V\w{6}', output)
            # 转换成集合去重
            sn = set(sn)
            # print(sn)
            # switch_sn = []
            # for i in sn:
            #     switch_sn.append(i)
            print(sn)


        except paramiko.ssh_exception.AuthenticationException:
            print("Failed to connect to", ip_address)
            switch_with_tacacs_issue.append(ip_address)
        except socket.error:
            print(ip_address, 'is not readable.')
            switch_not_rechable.append(ip_address)

        ssh_client.close()
# iplist.close()
if switch_with_tacacs_issue:
    print('\nTACACS is not working for below switches:')
    for i in switch_with_tacacs_issue:
        print(i)
if switch_not_rechable:
    print('\nBelow switches are not reachable:')
    for i in switch_not_rechable:
        print(i)
if switch_upgrade:
    print('\nBelow switches IOS version are up-to-date:')
    for i in switch_upgrade:
        print(i)
if switch_not_upgraded:
    print('\nBelow switches IOS version are not updated yet:')
    for i in switch_not_upgraded:
        print(i)
