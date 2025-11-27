---
title: "Containerd命令行管理工具"
date: 2025-11-27T10:51:50+08:00
draft: false
---

# Containerd 命令行管理工具


## 1、ctr 为Containerd自带的命令行管理工具
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

## 2、nerdctl (最接近docker CLI)
基本和docker CLI命令一致，只是在命令前添加了`nerdctl`前缀

```shell
#!/bin/bash
set -e

ARCH=amd64

VERSION=2.1.5

# 下载 nerdctl 安装包
wget https://github.com/containerd/nerdctl/releases/download/v${VERSION}/nerdctl-${VERSION}-linux-${ARCH}.tar.gz

# 解压
tar -xzvf nerdctl-${VERSION}-linux-${ARCH}.tar.gz

# 移动到 /usr/local/bin
sudo mv nerdctl /usr/bin

# 删除安装包
rm -f nerdctl-${VERSION}-linux-${ARCH}.tar.gz

# 删除 containerd-rootless 相关脚本
rm -rf containerd-rootless-setuptool.sh containerd-rootless.sh

echo "✅ nerdctl v${VERSION} 安装完成，可以直接运行 'nerdctl --version'"

```

## 3、Kubernetes 从 Docker 转向 containerd 的原因
###  架构层面的原因

kubelet 启动一个容器的流程:

> kubelet
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


- Docker Engine 是一个 完整平台（构建镜像、管理网络、Volume、Swarm 等），这些对 K8s 来说都是多余的。
- dockershim 只是为了把 CRI（K8s 语言）翻译成 Docker API（Docker 语言）。
- 实际执行容器的，依然是 containerd + runc。

当 kubelet 直接使用 containerd 时，调用链简化为：
> kubelet
  │
  │ (调用 CRI 接口)
  ▼
containerd (内置 CRI 插件)
  │
  │ (调用 OCI 接口)
  ▼
runc (OCI runtime)
  │
  └─> 真正创建 Linux 容器


### 减少维护成本
kubernetes 从 1.24 开始，默认使用 containerd 作为容器运行时。不再去维护中间dockershim

### 性能提升
少一层调用，性能和稳定性更好。