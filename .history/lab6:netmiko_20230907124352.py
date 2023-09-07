from netmiko import ConnectHandler

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
