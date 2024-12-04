# Introduction

<img src="./img/1.png" alt="image-20241204105423699" style="zoom:50%;" />

在这个演示中，我们将在 Linux 下通过一些命令行配置来操作路由表

我们提供了一个拓扑名为 mod2-play 的 containerlab 拓扑配置文件（3lan-mod2.clab.yml）。 其中有 3 台主机（分别名为 lan1、lan2 和 lan3）连接到 1 台路由器（名为 rtr）（路由器只是我们要配置的一台 Linux 主机）。 要启动容器，请运行以下命令。

```
sudo containerlab deploy
```

注意：完成后，如果想拆除实验室设置，请运行 `sudo containerlab destroy` 。

我们提供了 3 个示例脚本，每个脚本都说明了一件事。 每个脚本都提供一个 “create ”函数和一个 “delete”函数，让你可以运行一个脚本创建一个设置，然后删除该设置，再用另一个脚本重新创建。

```
./setup-ip-ex1.sh create
./setup-ip-ex1.sh delete
```

快捷别名指令

```
lan1="docker exec -it  clab-mod2-play-lan1"
```

 使用别名示例

```
$lan1 ip addr add 10.0.1.2 dev eth1
````

# Example 1: setup-ip-ex1.sh 

说明不使用 via 时的情况 

此脚本将为每台主机添加 IP 地址，并为 10.0.0.0/16 设置路由条目，但不使用 via。

尽管所有路由表都已设置，但从 lan1 Ping 到 lan3 应该无法正常工作，因为 lan* 路由表项假定它们是直接连接的（所以它会 ARP 目标地址）

```
lan1 ping 10.0.3.2
```
```
路由器的eth1不知道谁是10.0.3.2（需要路由器进行转发）
root@docker:~/linux-network/02-router/demo1-cli# lan1 ping 10.0.3.2
PING 10.0.3.2 (10.0.3.2) 56(84) bytes of data.
From 10.0.1.2 icmp_seq=1 Destination Host Unreachable
From 10.0.1.2 icmp_seq=2 Destination Host Unreachable
From 10.0.1.2 icmp_seq=3 Destination Host Unreachable
```
# Example 2: setup-ip-ex2.sh 

说明使用 via 时会发生什么。

从 lan1 Ping 到 lan3 可以正常工作，因为 lan* 路由表项现在表示要通过路由器

```
lan1 ping 10.0.3.2
```

# Example 3: setup-ip-ex3.sh

这将显示分配了多个 IP 地址的接口。


默认情况下，它会使用最先定义的 IP 地址（10.0.1.2）作为源地址。

```
lan1 ping 10.0.3.3
```

指定特定的源/目的

```
lan1 ping -I 10.0.1.3 10.0.3.3
```


# Example 4: setup-ip-ex4.sh 

说明如何设置 GRE 隧道。 

它创建了一个本地/远程指向 10.0.1.2/10.0.3.2 的 GRE 隧道（这是外层报头）

然后给设备一个不同前缀的地址 192.168.0.1/192.168.0.2（这是内标头）
```
root@docker:~/linux-network/02-router/demo1-cli# lan1  route   
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         172.20.20.1     0.0.0.0         UG    0      0        0 eth0
10.0.0.0        10.0.1.1        255.255.0.0     UG    0      0        0 eth1
10.0.1.1        0.0.0.0         255.255.255.255 UH    0      0        0 eth1
172.20.20.0     0.0.0.0         255.255.255.0   U     0      0        0 eth0
192.168.0.0     0.0.0.0         255.255.255.252 U     0      0        0 gre1

```

设置完成后，就可以 ping 192.168 前缀了：

```
lan1 ping 192.168.0.2
```

You can run tshark

```
# 这条命令的作用是：监听名为 gre1 的网络接口，并解码和显示通过该接口的所有 GRE 流量。 你将看到 GRE 头部信息，例如源 IP 地址、目标 IP 地址、协议类型等，以及 GRE 载荷中的数据（取决于封装的协议）。
root@docker:~/linux-network/02-router/demo1-cli# lan1 tshark -O gre -i gre1 
Running as user "root" and group "root". This could be dangerous.
Capturing on 'gre1'
 ** (tshark:221) 23:44:11.456352 [Main MESSAGE] -- Capture started.
 ** (tshark:221) 23:44:11.456460 [Main MESSAGE] -- File: "/tmp/wireshark_gre1LB3YX2.pcapng"
/////////
Frame 1: 100 bytes on wire (800 bits), 100 bytes captured (800 bits) on interface gre1, id 0
Linux cooked capture v1
Internet Protocol Version 4, Src: 192.168.0.1, Dst: 192.168.0.2
Internet Control Message Protocol


# will  have encapsulation
lan1 tshark -O gre -i eth1
root@docker:~/linux-network/02-router/demo1-cli# lan1 tshark -O gre -i eth1 
Running as user "root" and group "root". This could be dangerous.
Capturing on 'eth1'
 ** (tshark:195) 23:44:06.004348 [Main MESSAGE] -- Capture started.
 ** (tshark:195) 23:44:06.004473 [Main MESSAGE] -- File: "/tmp/wireshark_eth144R8X2.pcapng"
///////
Frame 1: 42 bytes on wire (336 bits), 42 bytes captured (336 bits) on interface eth1, id 0
Ethernet II, Src: aa:c1:ab:f2:37:28 (aa:c1:ab:f2:37:28), Dst: Broadcast (ff:ff:ff:ff:ff:ff)
Address Resolution Protocol (request)

Frame 2: 42 bytes on wire (336 bits), 42 bytes captured (336 bits) on interface eth1, id 0
Ethernet II, Src: aa:c1:ab:2d:83:47 (aa:c1:ab:2d:83:47), Dst: aa:c1:ab:f2:37:28 (aa:c1:ab:f2:37:28)
Address Resolution Protocol (reply)

Frame 3: 122 bytes on wire (976 bits), 122 bytes captured (976 bits) on interface eth1, id 0
Ethernet II, Src: aa:c1:ab:f2:37:28 (aa:c1:ab:f2:37:28), Dst: aa:c1:ab:2d:83:47 (aa:c1:ab:2d:83:47)
Internet Protocol Version 4, Src: 10.0.1.2, Dst: 10.0.3.2
Generic Routing Encapsulation (IP)
    Flags and Version: 0x0000
        0... .... .... .... = Checksum Bit: No
        .0.. .... .... .... = Routing Bit: No
        ..0. .... .... .... = Key Bit: No
        ...0 .... .... .... = Sequence Number Bit: No
        .... 0... .... .... = Strict Source Route Bit: No
        .... .000 .... .... = Recursion control: 0
        .... .... 0000 0... = Flags (Reserved): 0
        .... .... .... .000 = Version: GRE (0)
    Protocol Type: IP (0x0800)
Internet Protocol Version 4, Src: 192.168.0.1, Dst: 192.168.0.2
Internet Control Message Protocol


# See encapsulation as it traverses the router
rtr tshark -O gre -i eth1  
```

# Neighbor

Ex1 和 Ex2 与发送的 ARP 请求具体相关。 因此，在 ping 之前，用 `ip neigh` 查看 ARP 表也是合理的。

查看 ARP 表 - lan1 上的表应该是空的

````
lan1 ip neigh
````

进行 ping（查看第一个数据包是否为 ARP - 使用 tshark 查看）

```
lan1 ip neigh
```

它应该输出   10.0.1.1 dev eth1 lladdr aa:c1:ab:4e:9b:e5 REACHABLE

过一会儿

```
lan1 ip neigh
```

应输出（显示条目已过时）：    10.0.1.1 dev eth1 lladdr aa:c1:ab:4e:9b:e5 STALE

您可以明确刷新：（您将再次看到 ARP）

```
lan1 ip neigh flush all
```

