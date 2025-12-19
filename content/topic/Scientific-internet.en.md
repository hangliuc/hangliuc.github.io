---
date: 2025-12-05 08:38:33
draft: false
tags:
- Network
title: Scientific Internet Access
---

This setup tutorial is for personal learning purposes only and must not be used for illegal activities.

## Installation
[https://itlanyan.com/v2ray-tutorial/](https://itlanyan.com/v2ray-tutorial/)


## Client Usage
### iOS
Client Configuration: [https://itlanyan.com/v2ray-clients-download/](https://itlanyan.com/v2ray-clients-download/)

The iOS client uses v2box, which cannot be downloaded in China.

Create a new configuration directly.

Protocol (Protocol): Select VMess


### macOS
Client: Clash Verge Rev

Download Link: [https://github.com/clash-verge-rev/clash-verge-rev/releases](https://github.com/clash-verge-rev/clash-verge-rev/releases)

- Local Config
```yaml
port: 7890
socks-port: 7891
allow-lan: true
mode: rule
log-level: info
external-controller: :9090

proxies:
  - name: "My V2Ray"
    type: vmess
    server: x.x.x.x
    port: 12345
    uuid: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    alterId: 0
    cipher: auto
    # If you haven't configured tls/ws, ignore the following lines.
    # network: ws
    # ws-opts:
    #   path: "/"
    
proxy-groups:
  - name: PROXY
    type: select
    proxies:
      - "My V2Ray"

rules:
  - MATCH,PROXY
```

- Create a new subscription, and select "Local" (Local file) under the "Type" (Type) option.