#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Switch:

    def __init__(self):
        pass

    packages = []
    switch_list = []

    def check_address(self):
        pass

    def check_package(self):
        pass


# 交换机转发表
physical_port_a = [1, 3, -1, -1, -1, -1]
physical_port_b = [-1, 3, 2, 0, -1, -1]
physical_port_c = [1, -1, -1, 3, -1, -1]
physical_port_d = [-1, 1, 0, 2, -1, -1]
physical_port_e = [0, 2, -1, -1, -1, -1]
physical_port_f = [1, 3, -1, -1, -1, -1]
physical_port_g = [3, 2, -1, -1, -1, -1]


switch_port_dic = {0: physical_port_a, 1: physical_port_b,
                   2: physical_port_c, 3: physical_port_d,
                   4: physical_port_e, 5: physical_port_g,
                   6: physical_port_f}

# 数据包状态表 当前所在交换机
unique = [0]


# 初始化7台交换机
def init_switch(count=7):
    switch = [Switch() for i in range(count)]
    for j in range(count):
        switch[j].switch_list = switch_port_dic[j]
    return switch


def judge_input(abc):
    try:
        int(abc)
    except ValueError as e:
        return -1
    if isinstance(abc, int):
        return abc
    else:
        return -1


def address_process(source, destination):
    sour_net = source[0:2]
    sour_host = source[2:6]
    des_net = destination[0:2]
    des_host = destination[2:6]

    return int(sour_net[0]) * 2 + int(sour_net[1]) * 1, int(des_net[0]) * 2 + int(des_net[1]) * 1, \
           int(sour_host[0]) * 8 + int(sour_host[1]) * 4 + int(sour_host[2]) * 2 + int(sour_host[3]) * 1, \
           int(des_host[0]) * 8 + int(des_host[1]) * 4 + int(des_host[2]) * 2 + int(des_host[3]) * 1


def package_in_which_switch():
    for j in range(7):
        if switch[j].packages is not None:
            return j


def forward_process(source_host, destination_host, package):
    switch[destination_host].packages = package
    switch[source_host].packages = None


if __name__ == '__main__':

    switch = init_switch()
    # 输入基本信息
    source_address = input("请输入信源的地址：")
    destination_address = input("请输入信宿的地址：")
    data = input("Please makeup your data package:")

    # 地址及数据包处理
    sr = list(source_address)
    dr = list(destination_address)
    s_net, d_net, s_host, d_host = address_process(source=sr, destination=dr)
    package = sr + dr + list(data)

    # 转发过程
    print("数据包所在的交换机为：", s_host)
    switch[s_host].packages = package
    print("数据包所要发往的交换机为：", d_host)
    if s_net == d_net:

        # from the same level 查找源地址交换机的转发表
        if d_host in switch[s_host].switch_list:
            print("可以直接转发：" + str(s_host) + " -> " + str(d_host))
            forward_process(s_host, d_host, package)
            in_where = package_in_which_switch()
            if in_where == d_host:
                print("转发成功！")
                print("当前数据包在交换机：", in_where)
        else:
            print("不可以直接转发，转发给相邻节点")
            for i in switch[s_host].switch_list:
                if i != -1:
                    forward_process(s_host, i, package)
                    if d_host in switch[i].switch_list:
                        forward_process(i, d_host, package)
                        in_where = package_in_which_switch()
                        if in_where == d_host:
                            print("转发成功！")
                            print("当前数据包在交换机：", in_where)

    elif s_net == 1 and d_net == 2:
        print("from top to middle")
    elif s_net == 2 and d_net == 3:
        print("from middle to blow")
    elif s_net == 1 and d_net == 3:
        print("from top to blow")
    elif s_net == 3 and d_net == 1:
        print("form blow to top")
    elif s_net == 3 and d_net == 2:
        print("from blow to middle")
