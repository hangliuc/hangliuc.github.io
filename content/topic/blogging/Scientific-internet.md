---
title: "科学上网"
date: 2025-12-05T16:38:33+08:00
draft: false
categories:
    - Blog
tags:
    - Network
---
此搭建教程只用于个人学习，不可用于非法用途。

## 安装
https://itlanyan.com/v2ray-tutorial/


## 客户端使用
### ios
客户端配置：https://itlanyan.com/v2ray-clients-download/

ios 客户端采用v2box，中国区不能下载。

直接新建配置即可

协议 (Protocol)：选择 VMess


### mac
客户端：Clash Verge Rev

下载链接：https://github.com/clash-verge-rev/clash-verge-rev/releases

- Local Config
```yaml
port: 7890
socks-port: 7891
allow-lan: true
mode: rule
log-level: info
external-controller: :9090

proxies:
  - name: "我的V2Ray"
    type: vmess
    server: x.x.x.x
    port: 12345
    uuid: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    alterId: 0
    cipher: auto
    # 如果你没配置 tls/ws，下面这几行不用管。
    # network: ws
    # ws-opts:
    #   path: "/"
    
proxy-groups:
  - name: PROXY
    type: select
    proxies:
      - "我的V2Ray"

rules:
  - MATCH,PROXY
```

- 新建订阅，在 “类型” (Type) 那一栏，选择 “Local” (本地文件)


