import paramiko
import time
import getpass

username = input("Username:")
password = getpass.getpass("Password:")
for i in range(2, 7):
    ip = '192.168.80.' + str(i)
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ip, username=username,
                       password=password, look_for_keys=False)
    command = ssh_client.invoke_shell()
    print("已经成功登录交换机" + ip)
    command.send('config t\n')
    for i in range(11, 16):
        print("正在创建VLAN:" + str(i))
        command.send('vlan ' + str(i) + '\n')
        time.sleep(1.5)
        command.send('name Python_vlan' + str(i) + '\n')
        time.sleep(1)
    command.send('end\n')
    command.send('wr mem\n')
    time.sleep(2)
    output = command.recv(65535).decode('ascii')
    print(output)
    ssh_client.close()
