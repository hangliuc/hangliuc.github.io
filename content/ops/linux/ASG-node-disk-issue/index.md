---
title: "ASG Node 数据盘挂载失败"
date: 2025-12-01T11:45:14+08:00
draft: false
categories:
    - 运维
tags:
    - Troubleshooting
---

## 问题背景
data 数据盘挂载失败，日志文件会写入根盘，导致磁盘多次报警

内核还没有来得及刷新分区表生成 /dev/nvme1n1p1 设备文件，就执行mkfs 命令，导致格式化失败。

![disk_error.png](disk_error.png)

## 解决方法
```shell
...
yum install parted -y
mkdir -p /data
parted -s /dev/nvme1n1 -- mklabel gpt
parted -s /dev/nvme1n1 -- mkpart primary ext4 0% 100%
partprobe /dev/nvme1n1
udevadm settle
while [ ! -e /dev/nvme1n1p1 ]; do sleep 1; done
mkfs -t ext4 /dev/nvme1n1p1
mount /dev/nvme1n1p1 /data
echo '/dev/nvme1n1p1 /data ext4 defaults 0 0' >> /etc/fstab
...
```


##

### parted 中 0 与 0% 的区别
- **0**：表示强制要求分区从磁盘的 第 0 个字节/扇区 开始。

- **0%**：自动对齐，最佳对齐点 开始分区。parted 会自动跳过前面的保留空间，通常将起始位置设定在 扇区 2048 开始。

### partprobe /dev/nvme1n1
通知内核（Kernel）立即重读分区表

### udevadm settle
阻塞（暂停）脚本执行，直到 udev 处理完所有设备事件。
所有设备文件都创建好，脚本才能继续执行。


## 用户数据脚本
用户脚本位置：
/var/lib/cloud/instance/user-data.txt

日志位置：
/var/log/cloud-init-output.log