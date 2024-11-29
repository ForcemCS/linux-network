#! /usr/bin/env python3

#该脚本的功能是从命令行获取源 MAC、目标 MAC、网络接口和消息，然后构造一个包含指定信息的以太网数据包，并通过指定的网络接口发送出去。 它可以用于测试网络连接，发送自定义数据包等。
#./onepkt.py 00:11:22:33:44:55 aa:bb:cc:dd:ee:ff eth0 "My test message"
#这将会通过 eth0 接口发送一个目标 MAC 为 aa:bb:cc:dd:ee:ff，源 MAC 为 00:11:22:33:44:55，包含 "My test message" 的 TCP 数据包。 IP 地址和端口号是脚本中预设的。

import sys
from scapy.all import *


if __name__ == '__main__':
    usage_string = """Usage:
  onepkt.py <src-mac> <dst-mac> <iface> <msg>
    where <msg> is unique identifier for this message"""

    # total arguments
    if (len(sys.argv) != 5):
        sys.exit("Incorrect usage - num args.\n"+usage_string)

    src_mac = sys.argv[1]
    dst_mac = sys.argv[2]
    iface = sys.argv[3]
    msg = sys.argv[4]

    src_ip = "1.1.1.1"
    dst_ip = "2.2.2.2"
    sport = 1111
    dport = 2222


    

    pkt = Ether(dst=dst_mac, src=src_mac) / IP (src=src_ip, dst=dst_ip) / TCP(sport=sport, dport=dport) / msg

    #pkt.show()

    sendp(pkt, iface=iface)

    #sendp(Ether(dst="aa:bb:cc:11:11:33", src="aa:bb:cc:11:11:11") / IP()/"HELLO", iface='eth1.9')


