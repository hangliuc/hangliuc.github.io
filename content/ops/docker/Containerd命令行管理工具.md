---
title: "Containerd命令行管理工具"
date: 2025-11-27T10:51:50+08:00
draft: false
categories:
    - 运维
tags:
    - docker
    - containerd
weight: 1
---

# Containerd 命令行管理工具

## Kubernetes 从 Docker 转向 containerd 的原因
###  架构层面的原因

kubelet 启动一个容器的流程:

 ```shell
 kubelet
  │
  │ (调用 CRI 接口)
  ▼
dockershim (K8s 维护的 CRI 转换层)
  │
  │ (调用 Docker Engine API)
  ▼
Docker Engine
  │
  │ (调用 containerd API)
  ▼
containerd
  │
  │ (调用 OCI 接口)
  ▼
runc (OCI runtime)
  │
  └─> 真正创建 Linux 容器 (namespace, cgroups, rootfs...)
  ```


- Docker Engine 是一个 完整平台（构建镜像、管理网络、Volume、Swarm 等），这些对 K8s 来说都是多余的。
- dockershim 只是为了把 CRI（K8s 语言）翻译成 Docker API（Docker 语言）。
- 实际执行容器的，依然是 containerd + runc。

当 kubelet 直接使用 containerd 时，调用链简化为：
```shell
 kubelet
  │
  │ (调用 CRI 接口)
  ▼
containerd (内置 CRI 插件)
  │
  │ (调用 OCI 接口)
  ▼
runc (OCI runtime)
  │
  └─> 真正创建 Linux 容器 (namespace, cgroups, rootfs...)
  ```



### 减少维护成本
kubernetes 从 1.24 开始，默认使用 containerd 作为容器运行时。不再去维护中间dockershim

### 性能提升
少一层调用，性能和稳定性更好。

## ctr -- Containerd自带的命令行管理工具
```shell
# 列出所有命名空间
sudo ctr namespaces list

```

```shell
# 镜像相关命令
sudo  ctr -n=k8s.io images -h

```

**ctr 上传、拉取镜像时不支持登陆认证，只能通过--user携带用户密码操作**
```shell
sudo ctr -n=k8s.io images pull \
  --user <username>:<password> \
  myregistry.example.com/myrepo/nginx:latest
```

## nerdctl (最接近docker CLI)
基本和docker CLI命令一致，只是在命令前添加了`nerdctl`前缀

### 安装nerdctl
```shell
#!/bin/bash
set -e

VERSION=${VERSION:-2.2.0}

# 自动识别架构
ARCH=$(uname -m)
if [[ "$ARCH" == "x86_64" ]]; then
    ARCH="amd64"
elif [[ "$ARCH" == "aarch64" ]]; then
    ARCH="arm64"
else
    echo "Unsupported architecture: $ARCH"
    exit 1
fi

DOWNLOAD_URL="https://github.com/containerd/nerdctl/releases/download/v${VERSION}/nerdctl-${VERSION}-linux-${ARCH}.tar.gz"

echo "Downloading nerdctl v$VERSION for $ARCH"
wget  "$DOWNLOAD_URL" -O nerdctl.tgz

echo "Extracting..."
tar -xzf nerdctl.tgz

# 解压后会得到 nerdctl、containerd、runc 等二进制
# 一般 nerdctl 位于当前目录的 nerdctl
TARGET_DIR="/usr/local/bin"

echo "Moving binaries to $TARGET_DIR (require sudo)"
sudo mv nerdctl "${TARGET_DIR}/"


echo "Cleaning up…"
rm -f nerdctl.tgz

echo "🎉 nerdctl installation completed!"
echo "Version check:"
sudo ${TARGET_DIR}/nerdctl --version


```


To list local Kubernetes containers:

```shell
nerdctl --namespace k8s.io ps -a
```
