import time
import logging
from netmiko import ConnectHandler
import getpass

LOG_FILE = 'log_file.log'
TIME = time.strftime('%Y-%m-%d_%H-%M-%S')
IP_LIST_FILE = 'switch_ip.txt'


class Device:
    pass

    def __init__(self, ip, username, password, device_type):
        self.ip = ip
        self.username = username
        self.password = password
        self.device_type = ruijie_os
        self.conn = None

    def connect(self):
        """
        使用 Netmiko 库连接设备
        """
        info = {
            'device_type': self.device_type,
            'ip': self.ip,
            'username': self.username,
            'password': self.password
        }
        try:
            self.conn = ConnectHandler(**info)
            self.log('已连接', LOG_FILE)
            print(f"已连接到 {self.ip}")

        except Exception as e:
            self.log(f"连接失败：{e}", '')
            # print(f"连接到 {self.ip} 失败：{e}")
            self.log('备份失败：连接失败', LOG_FILE)  # 添加备份失败的日志信息
            return  # 连接失败，直接返回，不执行后续操作

    def log(self, message, log_file,):
        """
        记录日志信息
        """
        LOG_FORMAT = "{ip}-{TIME}-{message}"
        log_message = LOG_FORMAT.format(
            ip=self.ip,
            message=message
        )
        if log_file:
            with open(log_file, 'a') as log:
                log.write(f"{log_message}\n")
        else:
            print(log_message)

    def backup(self, log_file):
        """
        备份设备配置
        """
        file_name = f"{self.ip}-{TIME}-backup.cfg"
        output = self.conn.send_command('show run')
        with open(file_name, 'w') as backup_file:
            backup_file.write(output)
        self.log('配置备份成功', log_file)
        print("配置备份成功")


def main():
    """ Main program
    """
    username = input('请输入用户名：')
    password = getpass.getpass('请输入密码：')
    with open(IP_LIST_FILE, 'r') as f:
        for ip in f:
            ip = ip.strip()
            device = Device(ip, username, password, ruijie_os)
            device.connect()


if __name__ == '__main__':
    main()
