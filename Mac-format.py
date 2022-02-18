def mac_list():
    with open('mac_list.txt', 'r',encoding='utf-8') as macs:
        for mac in macs:
            if '.' in mac or '-' in mac or ':' in mac:
                mac1 = mac.strip().replace(":", "")  # 加.lower()变全小写
                mac_out = "-".join(mac1[i:i + 4] for i in range(0, len(mac1), 4))
                print(mac_out)
            else:
                print('mac地址输入错误!!!')
mac_list()
