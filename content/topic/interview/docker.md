---
title: "SRE面试题汇总 | Docker"
image: /img/cover/docker_interview_cover.png
date: 2025-12-06T09:56:07+08:00
draft: false
categories:
    - 面试
tags:
    - Docker
---
## 容器技术的基础原理
容器技术的基础原理是基于 Linux 内核的 Namespace、Cgroups、Rootfs、Capabilities 和 Seccomp 等机制。

它主要解决了应用运行环境不一致的问题：将应用、依赖和配置打包为可复用的镜像，再以隔离的进程方式运行。

容器镜像通常利用 Linux 的 Union FS 能力，将基础系统、运行库、应用文件和配置等内容以分层方式组织起来。容器启动时，运行时会把镜像层和可写层组合成容器的 Rootfs。

## 如何减小 Dockerfile 生成的镜像体积？
- 使用更小的基础镜像
- 将构建环境与运行环境分离，使用多阶段构建：
```dockerfile
# 第一阶段：编译
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /out/app .

# 第二阶段：运行
FROM alpine:3.19
COPY --from=builder /out/app /usr/local/bin/app
CMD ["/usr/local/bin/app"]
```

- 及时清理构建缓存和临时文件，并让 `apt`、`yum`、`apk` 的缓存不要进入最终镜像层。例如 Debian/Ubuntu 可以使用 `--no-install-recommends`。
- 合并关联的 `RUN` 指令，避免清理操作发生在下一层，导致缓存仍然保留在镜像历史中。
- 最终运行阶段只复制必要的二进制文件、配置和证书，不要复制整个源码目录。
- 使用 `.dockerignore` 排除 `.git`、测试数据、日志、构建产物和本地依赖等无关文件。
- 根据程序依赖选择基础镜像。Alpine 不一定适合所有程序，使用 C/C++ 或 CGO 时要注意 musl/glibc 兼容性；使用 `scratch` 或 distroless 时还要补充 CA 证书、时区等运行时文件。

## 容器网络模式
| 网络模式 | 特点 | 典型场景 |
| --- | --- | --- |
| `bridge` | 默认模式，容器拥有独立的 Network Namespace 和 IP，通过网桥通信；外部通常通过端口映射访问 | 普通 Web 服务、微服务，最常用 |
| `host` | 容器直接使用宿主机网络栈，没有独立的网络 Namespace，不经过常规 NAT | 对网络性能或端口可见性要求较高的场景 |
| `none` | 只保留 loopback，不配置外部网络，需要应用自行配置网络 | 强隔离或自定义网络实验 |
| `container:<name\|id>` | 与另一个容器共享 Network Namespace，共享 IP、端口和 `localhost` | Sidecar、多容器协作 |

`container` 模式下，两个容器访问对方通常使用 `localhost` 和共享端口，而不是把它们当成拥有两个独立 IP 的容器。

## Docker、镜像和 container 的区别

- **Docker / Docker Engine**：容器平台和容器引擎，负责镜像构建、容器创建与管理、网络、Volume 等能力。
- **镜像（Image）**：只读的分层模板，包含应用程序及其依赖、文件系统和默认配置，本身不是正在运行的进程。
- **容器（Container）**：镜像启动后的运行实例，本质上是一组被 Namespace 和 Cgroups 隔离、限制和管理的进程。
- **containerd**：负责镜像传输与存储、容器生命周期等核心工作的容器运行时；Docker Engine 内部也会使用 containerd。

## 为什么 Kubernetes 从 Docker Engine 转向 containerd？

Kubernetes 真正需要的是符合 CRI（Container Runtime Interface）的容器运行时，而 Docker Engine 是一个包含镜像构建、网络、Volume、Swarm 等能力的完整平台，并没有直接面向 kubelet 的原生 CRI 接口。

### 架构层面的原因

使用 Docker Engine 时，kubelet 启动容器通常需要经过 dockershim 转换层：

```text
kubelet
  │ 调用 CRI
  ▼
dockershim（Kubernetes 维护的 CRI 转换层）
  │ 调用 Docker Engine API
  ▼
Docker Engine
  │ 调用 containerd API
  ▼
containerd
  │ 调用 OCI Runtime
  ▼
runc（以 runc 为例）
  └─> 创建 Linux 容器（Namespace、Cgroups、Rootfs 等）
```

- Docker Engine 的很多平台能力对 kubelet 并不是必需的。
- dockershim 负责把 Kubernetes 的 CRI 调用转换为 Docker Engine API 调用，增加了维护成本和中间环节。
- 真正创建 Linux 容器的通常仍是 containerd 加 OCI Runtime，例如 runc。

当 kubelet 直接通过 CRI 使用 containerd 时，调用链可以简化为：

```text
kubelet
  │ 调用 CRI
  ▼
containerd（CRI 插件）
  │ 调用 OCI Runtime
  ▼
runc（以 runc 为例）
  └─> 创建 Linux 容器（Namespace、Cgroups、Rootfs 等）
```

### 减少维护成本

Kubernetes 1.24 移除了内置的 dockershim，不再在 Kubernetes 项目中维护 Docker Engine 的适配层。这里的含义不是 Kubernetes 强制所有集群使用 containerd，containerd、CRI-O 等符合 CRI 的运行时都可以使用；containerd 只是常见选择之一。

### 性能与稳定性

直接使用 CRI 运行时可以减少适配层和组件数量，降低维护复杂度，并可能减少额外的调用开销。但实际性能和稳定性还取决于运行时版本、CNI、存储驱动、镜像配置和工作负载，不能简单认为“少一层调用”就一定带来显著性能提升。
