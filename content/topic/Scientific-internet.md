---
title: "科学上网"
description: "记录基于 3x-ui 的个人代理服务搭建，以及 iOS、Android 和 macOS 客户端的配置方法。"
image: /img/cover/scientific_internet_cover.png
date: 2025-12-05T16:38:33+08:00
draft: false
tags:
    - Network
---

> 本文内容仅用于个人学习和访问公开技术资料。请遵守所在地区的法律法规，以及云服务商和网络服务商的使用条款。

## 安装服务端：3x-ui

当前使用 [3x-ui](https://github.com/MHSanaei/3x-ui) 管理 Xray 服务。它提供 Web 控制面板，可以创建和管理 VMess、VLESS、Trojan、Shadowsocks、WireGuard 等多种协议，并生成客户端配置、二维码和订阅链接。

### 安装

[3x-ui GitHub 官方仓库](https://github.com/MHSanaei/3x-ui)

### 创建入站并获取客户端配置

1. 使用安装结果中的地址和凭据登录 3x-ui 面板。
2. 进入 **入站 (Inbounds)**，新建一个入站配置。本文以 **VMess** 为例；端口、UUID、传输方式以及 TLS/Reality 等参数按自己的域名和服务器配置填写。
3. 保存配置后，在客户端列表中复制订阅链接，或使用面板生成的二维码、分享链接。
4. 将订阅链接或二维码导入客户端。客户端连接参数必须与 3x-ui 面板中的入站配置完全一致。

订阅链接、服务器地址、端口和 UUID 都属于敏感配置，不要提交到公开仓库、博客或聊天群。如果订阅链接已经泄露，请在面板中重新生成或撤销对应客户端。

## 客户端使用

### iOS

客户端选择和下载可参考 [V2Ray 客户端整理](https://itlanyan.com/v2ray-clients-download/)。当前使用 V2Box 时，中国区 App Store 可能无法直接下载，需要根据自己的账号地区选择可用客户端，并遵守相关服务条款。

配置方式优先选择从 3x-ui 导出的二维码或分享链接直接导入。手动添加时，可以按以下方式填写：

- **协议 (Protocol)**：选择 `VMess`
- **服务器、端口、UUID**：填写 3x-ui 入站配置中的值
- **传输方式、TLS、Host、Path 等**：与面板生成的客户端配置保持一致

导入完成后，选择该配置并连接；不要把服务器管理面板的用户名和密码填入客户端。

### Android

推荐使用 [NekoBoxForAndroid](https://github.com/MatsuriDayo/NekoBoxForAndroid)，也可以从其 [Releases 页面](https://github.com/MatsuriDayo/NekoBoxForAndroid/releases) 下载对应版本。

打开 NekoBox 后，可以通过二维码、`vmess://` 分享链接或订阅链接导入配置。导入后选择节点，启动 VPN，并访问一个可信的测试页面确认连接是否正常。

### macOS

推荐使用 [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev)，安装包位于其 [Releases 页面](https://github.com/clash-verge-rev/clash-verge-rev/releases)。

使用 3x-ui 订阅时：

1. 在 3x-ui 面板中复制客户端订阅链接。
2. 在 Clash Verge Rev 的 **订阅** 页面，将链接粘贴到“订阅文件链接”输入框。
3. 点击 **新建** 或导入，等待配置下载完成。
4. 更新订阅后，选择对应配置，并在 **代理** 页面选择节点。
5. 根据需要开启系统代理，选择规则模式或全局模式，然后访问可信网站测试。

如果只有单条 VMess 链接而没有 Clash 订阅，可使用 [在线订阅转换工具](https://sub.cmliussss.com/) 转换格式。订阅链接通常包含访问凭据，在线转换前应确认服务可信；更稳妥的方式是使用本地转换工具，并在使用临时订阅后及时撤销旧链接。

## 参考资料

- 旧版 [V2Ray 搭建教程](https://itlanyan.com/v2ray-tutorial/)：仅作背景参考，当前服务端安装以 3x-ui 官方文档为准。
- [3x-ui 官方仓库](https://github.com/MHSanaei/3x-ui)
