import paramiko
import time
import getpass
import sys
import socket

now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
username = input('username:')
password = getpass.getpass('password:')

# cmd_file = sys.argv[2]

switch_without_authentication_issue = []
switch_not_reached = []

with open('ip_list.txt', mode='r') as f:
    for line in f.readlines():
        try:
            ip = line.strip()
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=username,
                        password=password, look_for_keys=False)
            print(f"Connecting to {ip},{now}")
            command = ssh.invoke_shell()
            with open('g1_command.txt', mode='r') as f1:
                f1.seek(0)
                for i in f1.readlines():
                    command.send(f'{i}\n')
            time.sleep(2)
            output = command.recv(65535).decode('ASCII')
            print(output)
        except paramiko.ssh_exception.AuthenticationException:
            print(f"{ip}用户验证失败！{now}")
            switch_without_authentication_issue.append(ip)
        except socket.error:
            print(f"{ip}连接失败!{now}")
            switch_not_reached.append(ip)
    ssh.close()
print('\n下列交换机用户验证失败：')
for i in switch_without_authentication_issue:
    print(i)
print('\n下列交换机连接失败：')
for i in switch_not_reached:
    print(i)
