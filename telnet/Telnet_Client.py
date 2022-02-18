# -*- coding: utf-8 -*-
import time,datetime
from telnetlib import Telnet
import threading

hosts = ["192.168.234.201",'192.168.234.202','192.168.234.203','192.168.234.204']
user1 = 'admin'
password1 = 'admin'
cmds = ['sys','inter g0/0/10','dis cur']
dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
def Telnet_Client(ip, user, password, cmds):
    try:
        with Telnet(ip,23,timeout=1) as tn:
            tn.read_until(b'Username')
            tn.write(user.encode() + b'\n')  # 对交换机输入一定要encode
            tn.read_until(b'Password')
            tn.write(password.encode() + b'\n')
            print(f'登录成功{ip}')
            for cmd in cmds:
                tn.write(cmd.encode() + b'\n')
            readreply = tn.expect([], timeout=1)[2].decode().strip()  # 读回显
            with open('log.txt','a') as f:
                f.write(readreply)
    except Exception as e:
        print(f'{ip}登录失败')

if __name__ == '__main__':
    with open('log.txt', 'a') as f:
        f.write('操作时间是：')
        start_time = str(datetime.datetime.now())
        f.write('\n' + '-'*60 + '\n' + start_time + '\n' + '-'*60 + '\n')
    for host in hosts:
        t1 = threading.Thread(target=Telnet_Client,args=(host,user1,password1,cmds))
        t1.start()
        #Telnet_Client(host,user1,password1)

