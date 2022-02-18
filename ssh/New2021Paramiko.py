# -*- coding: utf-8 -*-
import paramiko
import time
from rich import print as rprint

ip = '192.168.56.11'
username = 'admin'
password = 'admin'
#paramiko.util.log_to_file('paramiko.log')#输出paramiko日志

def ssh_client():  # 连接设备函数
    try:
        ssh_client = paramiko.SSHClient()  # 实例化ssh客户端
        ssh_client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())  # 自动保存ssh公钥
        ssh_client.connect(hostname=ip, port=22, username=username, password=password,
                           timeout=3, look_for_keys=False)  # look_for_keys 检查本地私钥
        global cli
        cli = ssh_client.invoke_shell()  # 打开交互式命令行
        cli.send(b'screen-length 0 temporary \n')  # 不分屏，直接显示内容
        time.sleep(0.2)
        output = cli.recv(65535).decode()
        #print(output)
        rprint(f'[green]成功登录:{ip}[/]')
        return 1
    except Exception as e:
        rprint(f'{ip}[red]登录失败,失败原因:[/]{e}')
        return 0


def arp_bind():  # 绑定arp命令
    cli.send('system-view \n')
    cmd = 'arp static ' + arp_ip + ' ' + mac + ' \n'
    cli.send(cmd)  # 发送命令


def del_arp():  # 删除arp命令
    cli.send('system-view \n')
    cmd = 'undo arp static ' + arp_ip + ' \n'
    cli.send(cmd)  # 要配置的命令


def dis_arp_ip():  # 查看arp-ip命令
    cmd = 'dis arp network  ' + arp_ip + ' static \n'
    cli.send(cmd)
    time.sleep(0.5)
    if cli.recv_ready():
        output = cli.recv(65535).decode().strip()
        global line_ip
        for line_ip in output.split('\n'):
            if 'S--' in line_ip:
                #print(f'\n绑定结果:{line_ip}\n')
                return line_ip


def dis_arp_mac():  # 查看arp-mac命令
    cmd = 'dis arp static | include ' + mac + '  \n'
    cli.send(cmd)
    time.sleep(0.5)
    if cli.recv_ready():
        output = cli.recv(65535).decode().strip()
        global line_mac
        for line_mac in output.split('\n'):
            if 'S--' in line_mac:
                #print(f'\n绑定结果:{line_mac}\n')
                return line_mac


def dhcp_bind():  # 绑定dhcp命令
    cli.send('system-view \n')
    pass


def del_dhcp():  # 删除dhcp绑定命令
    cli.send('system-view \n')
    pass


def save():  # 保存配置命令
    cli.send(b'return \n')
    cli.send(b'save \n')
    cli.send(b'y \n')
    time.sleep(0.5)
    output = cli.recv(65535).decode()
    #print(output)
    rprint('[yellow]保存完成!!![/]\n')


def mac_format():  # 格式化mac地址
    global mac
    mac = input('请输入MAC地址:').strip()
    if '.' in mac:
        mac = mac.replace(".", "").lower()
        mac = "-".join(mac[i:i + 4]for i in range(0, len(mac), 4))
    elif '-' in mac:
        mac = mac.replace("-", "").lower()
        mac = "-".join(mac[i:i + 4]for i in range(0, len(mac), 4))
    elif ':' in mac:
        mac = mac.replace(":", "").lower()
        mac = "-".join(mac[i:i + 4]for i in range(0, len(mac), 4))
    else:
        print('输入错误，请重新输入!!!')
    return mac


def firewall_bind():  # 防火墙绑定地址
    cli.send('system-view \n')
    pass


if ssh_client() == 1:
    while 1:
        print('*'*50)
        print('用户绑定请按【1】用户变更请按【2】用户删除请按【3】\n查询地址请按【4】退出程序请按【q】')
        choose_type = input('请选择进入>>>:').strip()
        if choose_type == '1':
            print('\n'+'='*21+'用户绑定'+'='*21+'\n')
            arp_ip = input('请输入绑定的IP地址:').strip()
            if arp_ip in str(dis_arp_ip()):
                rprint(f'[yellow]该IP地址已经绑定:\n{line_ip}\n请核查后再操作!!![/]\n')
                continue
            elif arp_ip.lower() == 'q':
                continue
            else:
                mac_format()
                if mac in str(dis_arp_mac()):
                    rprint(f'[yellow]该MAC地址已经绑定:\n{line_mac}\n请核查后再操作!!![/]\n')
                    continue
                elif mac.lower() == 'q':
                    continue
                else:
                    arp_bind()
                    rprint(f'\n[yellow]绑定结果:\n{dis_arp_ip()}\n[/]')
                    rprint('[green]绑定已经完成！正在保存...请勿退出!\n[/]')
                    save()
                    continue

        elif choose_type == '2':
            print('\n'+'='*22+'用户变更'+'='*22+'\n')
            arp_ip = input('请输入变更的IP地址:').strip()
            if arp_ip in str(dis_arp_ip()):
                rprint(f'[red]该IP地址已经绑定的MAC地址:\n{line_ip}\n[/]')
                y1 = input('是否要更改?是【y】否【n】')
                if y1.lower() == 'y':
                    mac_format()
                    if mac in str(dis_arp_mac()):
                        rprint(f'[red]该MAC地址已经绑定的IP地址:\n{line_mac}\n[/]')
                        y2 = input('是否要更改?是【y】否【n】')
                        if y2.lower() == 'y':
                            arp_bind()
                            rprint(f'\n[yellow]绑定结果:\n{dis_arp_ip()}\n[/]')
                            rprint('[green]绑定已经完成！正在保存...请勿退出!\n[/]')
                            save()
                            continue
                        elif y2.lower() == 'n':
                            continue
                        else:
                            rprint('[red]输入有错误, 请重新输入!\n[/]')
                            continue
                    else:
                        arp_bind()
                        rprint(f'\n[yellow]绑定结果:\n{dis_arp_ip()}\n[/]')
                        rprint('[green]绑定已经完成！正在保存...请勿退出!\n[/]')
                        save()
                        continue
                elif y1.lower() == 'n':
                    continue
                else:
                    rprint('[red]输入有错误, 请重新输入!\n[/]')
                    continue

            elif arp_ip.lower() == 'q':
                continue
            else:
                print(str(dis_arp_ip()))
                rprint('[red]该IP地址没有静态绑定,请核查后再操作!!![/]\n')
                continue
        elif choose_type == '3':
            print('\n'+'='*22+'用户删除'+'='*22+'\n')
            arp_ip = input('请输入要删除的IP地址:').strip()
            if arp_ip in str(dis_arp_ip()):
                rprint(f'\n[yellow]绑定结果:\n{dis_arp_ip()}\n[/]')
                y3 = input('是否要删除?是【y】否【n】')
                if y3 == 'y':
                    del_arp()
                    rprint(f'\n[yellow]绑定结果:\n{dis_arp_ip()}\n[/]')
                    rprint('\n[red]删除已经完成！正在保存...请勿退出![/]\n')
                    save()
                    continue
                elif y3 == 'n':
                    continue
                else:
                    rprint('\n[red]输入有错误,请重新输入!!![/]\n')
                    continue
            elif arp_ip.lower() == 'q':
                continue
            else:
                rprint(f'\n[yellow]绑定结果:\n{dis_arp_ip()}\n[/]')
                rprint('\n[red]该IP地址没有静态绑定!!![/]\n')
                continue

        elif choose_type == '4':
            print('\n'+'='*22+'查询地址'+'='*22+'\n')
            ip_or_mac = input('要查询IP还是MAC?IP【1】MAC【2】')
            if ip_or_mac == '1':
                arp_ip = input('请输入查询的IP地址：')
                print('该IP地址绑定情况如下:')
                if arp_ip in str(dis_arp_ip()):
                    rprint(f'\n[yellow]绑定结果:\n{dis_arp_ip()}\n[/]')
                    continue
                else:
                    rprint(f'\n[yellow]绑定结果:\n{dis_arp_ip()}\n[/]')
                    rprint('\n[red]该IP地址没有静态绑定![/]\n')
                    continue
            elif ip_or_mac == '2':
                mac_format()
                print('该MAC地址绑定情况如下:')
                if mac in str(dis_arp_mac()):
                    rprint(f'\n[yellow]绑定结果:\n{dis_arp_mac()}\n[/]')
                    continue
                else:
                    rprint(f'\n[yellow]绑定结果:\n{dis_arp_ip()}\n[/]')
                    rprint('\n[red]该IP地址没有静态绑定![/]\n')
                    continue
            elif arp_ip.lower() == 'q':
                continue
            else:
                rprint('\n[red]输入有错误,请重新输入![/]\n')
                break

        elif choose_type.lower() == 'q':
            print('\n'+'*'*22+'已退出'+'*'*22+'\n')
            cli.close()
            break
        else:
            rprint('[red]\n'+'*'*15+'输入错误，请重新输入!'+'*'*15 + '\n[/red]')
            continue
