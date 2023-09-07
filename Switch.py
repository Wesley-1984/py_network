import time
from netmiko import ConnectHandler
from getpass import getpass

LOG_FILE = 'log_file.log'
CMD_FILE = '../cmd_file.txt'
IP_LIST_FILE = '../ip_list.txt'
TFTP_SERVER = '192.168.1.1'
FIRMWARE_FILE = 'S29_RGOS11.4(1)B74P9_install.bin'
DEVICE_TYPE = 'cisco_ios'


class Device:
    """
    设备类
    定义了设备连接函数,核实IP_LIST_FILE
    日志函数，日志报错、配置信息、固件更新等都会保存到log_file中
    更新固件函数,请修改全局变量TFTP_SERVER和FIRMWARE_FILE
    执行配置命令函数，cmd_file特权模式下运行的脚本
    设备备份函数，设备备份产生以ip和日期为名称创建文件
    想要执行哪个功能按函数分类选择
    """

    def __init__(self, ip, username, password, device_type):
        self.ip = ip
        self.username = username
        self.password = password
        self.device_type = device_type
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

    def log(self, message, log_file):
        """
        记录日志信息
        """
        LOG_FORMAT = "{ip}-{time}-{message}"
        log_message = LOG_FORMAT.format(
            ip=self.ip,
            time=time.strftime('%Y-%m-%d %H:%M:%S'),
            message=message
        )
        if log_file:
            with open(log_file, 'a') as log:
                log.write(f"{log_message}\n")
        else:
            print(log_message)

    def upgrade_firmware(self, tftp_server, firmware_file, log_file):
        """
        使用 TFTP 服务器升级设备固件
        """
        tftp_path = f"tftp://{tftp_server}/{firmware_file}"
        flash_path = f"flash:/{firmware_file}"
        upgrade_cmd = f"upgrade {flash_path}"
        try:
            output = self.conn.send_command(
                f'copy {tftp_path} {flash_path}',
                upgrade_cmd,
                'y',
                read_timeout=300,
                use_textfsm=False  # 不使用 TextFSM 进行解析
            )
            print(f"{self.ip} 固件升级成功")
            print(output)
            with open(f'{self.ip}_update_info.csv', 'a') as csv_file:
<<<<<<< HEAD
                csv_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')},{output}\n")
=======
                csv_file.write(
                    f"{time.strftime('%Y-%m-%d %H:%M:%S')},{output}\n")
>>>>>>> 2054dc0 (first commit)
                self.log('升级成功', log_file)
        except Exception as e:
            print(f"{self.ip} 固件升级失败：{e}")
            self.log(f"升级失败：{e}", log_file)

    def execute(self, cmd, log):
        """
        在设备上执行命令并记录输出
        """
        log_message = f"Command: {cmd}\n"
        output1 = self.conn.send_config_set(cmd)
        log_message += f"{output1}\n"
        output2 = self.conn.send_command('show interfaces transceiver diagn')
        log_message += f"{output2}\n"
        self.log(f"配置保存成功{log_message}", log)
        print(f"配置保存成功{log_message}")

    def backup(self, log_file):
        """
        备份设备配置
        """
        backup_time = time.strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f"{self.ip}-{backup_time}-backup.cfg"
        output = self.conn.send_command('show run')
        with open(file_name, 'w') as backup_file:
            backup_file.write(output)
        self.log('配置备份成功', log_file)
        print("配置备份成功")


def main():
    """ Main program
    """
    username = input('请输入用户名：')
    password = getpass('请输入密码：')
    with open(CMD_FILE, 'r') as f:
        cmd_file = f.read().splitlines()

    with open(IP_LIST_FILE, 'r') as f:
        for ip in f:
            ip = ip.strip()
            device = Device(ip, username, password, DEVICE_TYPE)
            device.connect()
            if device.conn:
                device.execute(cmd_file, LOG_FILE)
                device.upgrade_firmware(TFTP_SERVER, FIRMWARE_FILE, LOG_FILE)
                device.backup(LOG_FILE)
<<<<<<< HEAD
=======
# TODO:调用方面还需要完善
>>>>>>> 2054dc0 (first commit)


if __name__ == '__main__':
    main()
