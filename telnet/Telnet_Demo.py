# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import time
from telnetlib import Telnet
import concurrent.futures


hosts = ["192.168.234.201", '192.168.234.202',
         '192.168.234.203', '192.168.234.204']
user1 = 'admin'
password1 = 'admin'
cmds = ['sys', 'inter g0/0/10', 'dis ver']

def Telnet_Client(ip, user=user1, password=password1, cmds=cmds):
    try:
        with Telnet(ip, 23, timeout=1) as tn:
            tn.read_until(b'Username')
            tn.write(user.encode() + b'\n')  # 对交换机输入一定要encode
            tn.read_until(b'Password')
            tn.write(password.encode() + b'\n')
            print(f'登录成功{ip}')
            for cmd in cmds:
                tn.write(cmd.encode() + b'\n')
            readreply = tn.expect([], timeout=1)[2].decode().strip()  # 读回显
            with open('log.txt', 'a') as f:
                f.write(readreply)
    except Exception as e:
        print(f'{ip}登录失败')


if __name__ == '__main__':
    t1 = time.time()
        #Telnet_Client(host,user1,password1)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        res = executor.map(Telnet_Client,hosts)
        print(res)
    t2 = time.time()
    print(t2-t1)
