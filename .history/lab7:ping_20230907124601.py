import os


"""
Python自带的ping模块显示一些无效的信息
"""
# ip = 'www.baidu.com'
# result = os.system('ping -c 10 ' +ip)	#linux
# # os.system('ping -n 10 ' +ip)	#windows
# if result == 0:
# 	print(ip+'可达')
# else:
# 	print(ip+'不可达‘）

for i in range(2, 7):
    ip = '192.168.2.'+str(i)
    result = os.system('ping -c 5'+ip)
    if result == 0:
        print(ip+'可达')
    else:
        print(ip+'不可达')
