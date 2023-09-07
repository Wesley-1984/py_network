from napalm import get_network_driver
import json
from getpass import getpass

ip = '192.168.80.2'
username = input('Username:')
password = getpass('Password:')

driver = get_network_driver('ios')
SW = driver(ip, username, password)
SW.open()
output = SW.get_interfaces()
# print(json.dumps(output,indent=2))
print(f'\n交换机{ip}的下列端口的端口状态为up/up：\n')
for key, value in output.items():
    if value['is_up']:
        print(key+'\tMAC address is\t'+value['mac_address'])
