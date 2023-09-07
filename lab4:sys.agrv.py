import paramiko
import time
import getpass
import sys

username = input('Username:')
password = getpass.getpass('Password:')
ip_file = sys.argv[1]
cmd_file = sys.argv[2]
with open(ip_file, 'r') as f:
    for line in f.readlines():
        ip = line.strip()
        # print(ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(ip, username=username,
                        password=password, look_for_keys=False)
            command = ssh.invoke_shell()
            print(f'{ip} is connected')
            with open(cmd_file, mode='r') as f:
                f.seek(0)
                for line in f.readlines():
                    command.send(line)
                    time.sleep(1)
                output = command.recv(65535).decode('ASCII')
                print(output)
        except Exception as e:
            print(f'{ip} is not connected')
            print(e)
        finally:
            ssh.close()
