import paramiko
import time
import getpass

# 输入用户名和密码
username = input('Username:')
password = getpass.getpass('Password:')

with open('ip_list.txt', mode='r', encoding='utf-8') as f:
    for line in f.readlines():
        ip = line.strip()
        # 创建SSH客户端对象
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            # 连接SSH服务器
            ssh_client.connect(hostname=ip, username=username,
                               password=password, look_for_keys=False)
            # 执行命令
            command = ssh_client.invoke_shell()
            print(f'{ip} is connected')
            command.send('conf t\n')
            command.send('router eigrp 1\n')
            time.sleep(1)
            command.send('end\n')
            command.send('wr mem\n')
            time.sleep(2)
            # 获取输出
            output = command.recv(65535).decode('ASCII')
            print(output)
        except Exception as e:
            print(f'{ip} is not connected')
            print(e)
            break
        finally:
            # 关闭SSH连接
            ssh_client.close()
