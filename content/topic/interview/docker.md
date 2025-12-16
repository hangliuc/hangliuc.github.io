---
title: "SRE面试题汇总 | Docker"
date: 2025-12-06T09:56:07+08:00
draft: false
categories:
    - 面试
tags:
    - Docker
---
## 1.容器技术的基础原理
容器技术的基础原理是基于 Linux 内核的 Namespace 和 Cgroups 技术。

解决问题：最初解决本地与云端不一致版本问题

容器镜像：利用Linux的Union FS技术，将应用程序所依赖的运行操作系统、工具包、依赖库、配置文件、运行脚本等各种环境信息以分层的方式联合挂载到同一个目录下，作为镜像的根目录

## 2.如何减⼩dockerfile⽣成镜像体积（多阶段构建）
- 使用更小的基础镜像
- 构建环境（编译器、依赖）与运行环境分离
```dockerfile
# 第一阶段：编译
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o app .

# 第二阶段：运行
FROM alpine:3.19
COPY --from=builder /app/app /usr/local/bin/app
CMD ["app"]
```
- 及时清理构建缓存、临时文件
- 合并 RUN 指令，减少镜像层数
- 不要复制整个项目 → 精准 COPY
- 使用 .dockerignore，避免复制不必要的文件
- ....

## 3.容器网络模式
- bridge：默认模式，容器之间可以通过 IP 通信，外部可以通过端口映射访问容器
- host：容器与主机共享网络栈，容器直接使用主机的 IP 和端口
- none：容器没有网络，只能使用 localhost 访问
- container：容器与另一个容器共享网络栈，容器之间可以直接通过 IP 通信

## 4.docker和container区别
- docker：是一个容器引擎，用于创建、运行、管理容器
- container：是一个运行中的进程，是一个独立的、可执行的软件包，包含应用程序和其依赖的运行环境

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