# -*- coding: utf-8 -*-
from netmiko import ConnectHandler
from rich import print as rprint
import time

def ssh_client():#连接设备函数
    host = '172.16.0.1'
    print('正在连接核心交换机%s' % host)
    device = {
        'device_type': 'huawei',
        'ip': host,
        'username': 'admin',
        'password': 'itcastADMIN1qaz',
        'global_delay_factor': 0.1,#全局影响引子
    }
    global net_connect
    with ConnectHandler(**device) as net_connect:
    #net_connect = ConnectHandler(**device)# 连接远程主机
        print(net_connect.find_prompt())

def arp_bind():#绑定arp命令
    config_arp = ('arp static ' + str(arp_ip) + ' ' + str(mac))
    # 要配置的命令
    in_put_arp = net_connect.send_config_set(config_arp)
    # 提交要配置的命令，in_put为提交的真实内容

def del_arp():  # 删除arp命令
    del_arp = ('undo arp static ' + ' ' + str(arp_ip))# 要配置的命令
    in_put_delarp = net_connect.send_config_set(del_arp)
    #net_connect.send_command('return')

def dis_arp():  # 查看arp命令
    out_put_disarp = net_connect.send_command('dis arp network  ' + str(arp_ip))
    print(out_put_disarp)

def dhcp_bind():#绑定dhcp命令
    pass

def del_dhcp():  # 删除dhcp绑定命令
    pass



def save(): #保存配置命令
    net_connect.send_command_timing('return')
    net_connect.send_command_timing('save')
    net_connect.send_command_timing('y')
    rprint('\n 保存完成！\n')


def mac_format(): #格式化mac地址
    global mac
    mac = input('请输入绑定的MAC地址：')
    if '.' in mac:
        mac = mac.strip().replace(".","").lower()
        mac = "-".join(mac[i:i + 4]for i in range(0, len(mac), 4))
    elif '-' in mac:
        mac = mac.strip().replace("-","").lower()
        mac = "-".join(mac[i:i + 4]for i in range(0, len(mac), 4))
    elif ':' in mac:
        mac = mac.strip().replace(":","").lower()
        mac = "-".join(mac[i:i + 4]for i in range(0, len(mac), 4))
    else:
        print('输入错误，请重新输入!!!')
    return mac


def firewall_bind():  # 防火墙绑定地址
    pass


while 1:
    ssh_client()
    print('\n' + '*'*50 + '\n')
    print('用户绑定请按【1】用户变更请按【2】用户删除请按【3】\n查询地址请按【4】退出程序请按【q】')
    choose_type = input('请选择进入>>>:').strip()
    if choose_type == '1':
        print('='*21+'用户绑定'+'='*21)
        arp_ip = input('请输入绑定的IP地址：')
        out_put = net_connect.send_command(
            'dis arp network ' + str(arp_ip) + 'static')
        if str(arp_ip) in out_put:
            print(out_put)
            rprint('\n[red]该IP地址已经绑定，请核查后再操作!!![/red]\n')
            break
        else:
            mac_format()
            out_put = net_connect.send_command(
                'dis arp static | include ' + str(mac1))
            if str(mac1) in out_put:
                print(out_put)
                rprint('\n[red]该MAC地址已经绑定，请核查后再操作!!![/red]\n')
                break
            else:
                arp_bind()
                dis_arp()
                rprint('\n[red]绑定已经完成！正在保存...请勿退出!!![/red]\n')
                save()
                break

    elif choose_type == '2':
        print('='*22+'用户变更'+'='*22)
    elif choose_type == '3':
        print('='*22+'用户删除'+'='*22)
    elif choose_type == '4':
        print('='*22+'查询地址'+'='*22)

    elif choose_type == 'q':
        print('*'*22+'已退出'+'*'*22)
        break
    elif choose_type == 'Q':
        print('*'*22+'已退出'+'*'*22)

        break
    else:
        rprint('[red]\n'+'*'*15+'输入错误，请重新输入!'+'*'*15 + '\n[/red]')
        continue
