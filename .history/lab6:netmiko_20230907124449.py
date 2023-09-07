from netmiko import ConnectHandler

"""
介绍：
1. Netmiko简化了show命令的执行和回显内容的读取
2. 简化了网络设备的配置命令
3. 支持多厂商的设备
4. Netmiko不需要import time模块，已经简化了
5. ConnectHandler 是Netmiko  ssh登录交换机连接器函数，相当paramiko的ssh.client，参数内容相差比较大
"""
S2 = {'device_type': 'ruijie_os',
      'ip': '192.168.80.3',
      'username': 'ruijie',
      'password': 'ruijie@123'
      }
conn = ConnectHandler(**S2)
print(f"已经成功登录交换机{S2['ip']}")
# 直接输入配置命令，不需要int ter
config_commands = ['int loop 1', 'ip add 2.2.2.2 255.255.255.255']
conn.send_config_set(config_commands)
print(output)  # 直接打印机屏幕

result = conn.send_command('show run int loop 1')  # 全局特权模式,只支持单条命令
conn.send_command('wr mem')
print(result)
