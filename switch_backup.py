#!/opt/switch/tutorial-env python3
# coding=utf-8
import os
import time
import datetime
from netmiko import ConnectHandler

"""
自动化定时备份交换机配置
"""


class RuijieSwitchBackup:
    def __init__(self, ip, username, password, save_path):
        self.ip = ip
        self.username = username
        self.password = password
        self.save_path = save_path

    def connect(self):
        device = {
            'device_type': 'ruijie_os',
            'ip': self.ip,
            'username': self.username,
            'password': self.password,
        }
        try:
            self.connection = ConnectHandler(**device)
            self.connection.enable()
        except Exception as e:
            self.log(f"Failed to connect to {self.ip}: {str(e)}")
            return False
        return True

    def backup_config(self):
        if not self.connect():
            return

        now = datetime.datetime.now()
        date_str = now.strftime("%Y%m")
        backup_filename = f"{self.ip}.text"
        full_backup_path = os.path.join(self.save_path, backup_filename)

        try:
            output = self.connection.send_command("show running-config")
            with open(full_backup_path, "w") as backup_file:
                backup_file.write(output)
            self.log(
                f"Backup completed for {self.ip}. Saved to {full_backup_path}")
        except Exception as e:
            self.log(f"Failed to backup {self.ip}: {str(e)}")
        finally:
            self.connection.disconnect()

    def log(self, message):
        log_filename = "backup_log.txt"
        log_message = f"[{datetime.datetime.now()}] {message}\n"
        with open(log_filename, "a") as log_file:
            log_file.write(log_message)


def main():
    # 从文本文件中读取IP地址列表
    ip_list_file = "/opt/switch/switch_ip.txt"
    save_directory = "./backup"
    username = 'ruijie'
    password = 'Your Password'

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    with open(ip_list_file, "r") as file:
        for line in file:
            ip = line.strip()
            switch = RuijieSwitchBackup(ip, username, password, save_directory)
            switch.backup_config()


if __name__ == '__main__':
    main()
