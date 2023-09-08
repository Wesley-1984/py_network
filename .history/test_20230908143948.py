import time
import schedule
from datetime import datetime
import logging
from netmiko import ConnectHandler

# 配置设置
USERNAME = '用户名'
PASSWORD = '密码'
BACKUP_FOLDER = '备份文件夹路径'
IP_LIST_FILE = 'switch_ip.txt'  # 存储交换机IP地址的文件
LOG_FILE = 'backup_log.txt'  # 日志文件

# 配置日志记录
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def backup_switch(ip):
    # 连接交换机
    device = {
        'device_type': 'ruijie_os',
        'ip': ip,
        'username': USERNAME,
        'password': PASSWORD,
    }

    try:
        ssh_connection = ConnectHandler(**device)
        ssh_connection.enable()  # 进入特权模式

        # 执行备份命令
        output = ssh_connection.send_command("show running-config")
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_filename = f"{BACKUP_FOLDER}/{ip}_backup_{current_time}.txt"

        # 保存备份到文件
        with open(backup_filename, 'w') as backup_file:
            backup_file.write(output)

        logging.info(f"{ip} 备份成功，已保存到 {backup_filename}")

    except Exception as e:
        logging.error(f"{ip} 备份失败：{str(e)}")


def main():
    # 从文件中读取IP地址列表
    with open(IP_LIST_FILE, 'r') as ip_file:
        ip_addresses = [line.strip() for line in ip_file.readlines()]

    # 遍历IP地址列表并为每个设备执行备份
    for ip in ip_addresses:
        backup_switch(ip)


# 安排每月的备份任务
schedule.every().month.at('01:00').do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
