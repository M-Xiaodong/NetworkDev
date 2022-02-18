# -*- coding: utf-8 -*-
import paramiko
import time
import multiprocessing

def ssh_client(ip,username,password,cmds,port=22):
    try:
        ssh_client = paramiko.SSHClient()  # 实例化ssh客户端
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 自动保存ssh公钥
        ssh_client.connect(hostname=ip, port=port, username=username,password=password, timeout=3,look_for_keys=False)  # look_for_keys 检查本地私钥
        command = ssh_client.invoke_shell()  # 打开交互式命令行
        command.send(b'screen-length 0 temporary \n')#不分屏，直接显示内容
        print(f'成功登录{ip}')
        for cmd in cmds:
            print(f'正在输入{cmd}')
            command.send(cmd + '\n')# 发送命令
            time.sleep(0.1)
            output = command.recv(65535).decode('ascii')
            print(output)
    except Exception as e:
        print(f'{ip}登录失败,失败原因{e}')


if __name__ == '__main__':
    ip_list = ['192.168.234.201', '192.168.234.202','192.168.234.203', '192.168.234.204']
    username = 'admin'
    password = 'admin'
    cmds = ['dis device','dis clock']
    for ip in ip_list:
        # t1 = threading.Thread(target=ssh_client,args=(ip,username,password,cmds))
        # t1.start()
        p1 = multiprocessing.Process(target=ssh_client,args=(ip,username,password,cmds))
        p1.start()

        
