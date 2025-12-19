---
categories:
- Interview
date: 2025-12-06 01:56:07
draft: false
tags:
- Docker
title: SRE Interview Questions Summary | Docker
---

## 1. Basic Principles of Container Technology
The basic principles of container technology are based on Linux kernel features such as Namespaces and Cgroups.

Problem-solving: Initially, it addressed the issue of inconsistent versions between local and cloud environments.

Container Images: Utilizing Linux's Union FS technology, the application's running operating system, toolset, dependency libraries, configuration files, runtime scripts, and other environmental information are layered and mounted to the same directory as the root directory of the image.

## 2. How to Reduce Dockerfile Image Size (Multi-Stage Builds)
- Use smaller base images
- Separate build environment (compilers, dependencies) from runtime environment
```dockerfile
# First stage: Compilation
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o app .

# Second stage: Runtime
FROM alpine:3.19
COPY --from=builder /app/app /usr/local/bin/app
CMD ["app"]
```
- Clean up build caches and temporary files in a timely manner
- Merge RUN commands to reduce the number of image layers
- Do not copy the entire project → Copy precisely
- Use .dockerignore to avoid copying unnecessary files
- ....

## 3. Container Network Models
- bridge: Default mode, containers can communicate with each other via IP, and external access can be achieved through port mapping
- host: Containers share the host's network stack, and containers use the host's IP and port directly
- none: Containers have no network, and can only be accessed using localhost
- container: Containers share a network stack with another container, and containers can communicate directly via IP

## 4. Difference Between Docker and Container
- Docker: A container engine used for creating, running, and managing containers
- Container: A running process, an independent, executable software package that includes the application and its runtime environment

### Architectural Reasons

The process of kubelet starting a container:

```shell
kubelet
  │
  │ (Calls CRI interface)
  ▼
dockershim (K8s-maintained CRI translation layer)
  │
  │ (Calls Docker Engine API)
  ▼
Docker Engine
  │
  │ (Calls containerd API)
  ▼
containerd
  │
  │ (Calls OCI interface)
  ▼
runc (OCI runtime)
  │
  └─> Create Linux container (namespace, cgroups, rootfs...)
```

- Docker Engine is a complete platform (building images, managing networks, volumes, Swarm, etc.), which is redundant for K8s.
- dockershim is only to translate the CRI (K8s language) into Docker API (Docker language).
- The actual execution of containers is still containerd + runc.

When kubelet uses containerd directly, the call chain simplifies to:
```shell
kubelet
  │
  │ (Calls CRI interface)
  ▼
containerd (Built-in CRI plugin)
  │
  │ (Calls OCI interface)
  ▼
runc (OCI runtime)
  │
  └─> Create Linux container (namespace, cgroups, rootfs...)
```

### Reducing Maintenance Costs
Starting from Kubernetes 1.24, containerd is used as the default container runtime by default. The maintenance of the intermediate dockershim is no longer required.

### Performance Improvement
Fewer layers of calls, better performance and stability.