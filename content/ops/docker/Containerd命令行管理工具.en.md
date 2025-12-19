---
categories:
- Operations Maintenance
date: 2025-11-27 02:51:50
draft: false
tags:
- Docker
- containerd
title: Containerd Command Line Management Tool
---

# Containerd Command Line Management Tool

## Reasons for Kubernetes to Shift from Docker to containerd

### Architectural Reasons

The process of starting a container by kubelet:

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
  └─> Truly create Linux container (namespace, cgroups, rootfs...)
  ```


- Docker Engine is a complete platform (building images, managing network, Volume, Swarm, etc.), which are redundant for K8s.
- dockershim is only for translating the CRI (K8s language) into Docker API (Docker language).
- The actual execution of containers is still containerd + runc.

When kubelet directly uses containerd, the call chain is simplified to:
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
  └─> Truly create Linux container (namespace, cgroups, rootfs...)
  ```



### Reducing Maintenance Costs
Starting with Kubernetes 1.24, containerd is used as the default container runtime. The intermediate dockershim is no longer maintained.

### Performance Improvement
Fewer layers of calls, better performance and stability.


## ctr -- Containerd's Built-in Command Line Management Tool
```shell
# List all namespaces
sudo ctr namespaces list

```

```shell
# Image-related commands
sudo ctr -n=k8s.io images -h

```

**ctr does not support login authentication for uploading and pulling images; it can only be operated with --user carrying the user password**
```shell
sudo ctr -n=k8s.io images pull \
  --user <username>:<password> \
  myregistry.example.com/myrepo/nginx:latest
```

## nerdctl (Most Similar to docker CLI)
Basic commands are consistent with docker CLI, with the prefix `nerdctl` added to the commands.

### Installing nerdctl
```shell
#!/bin/bash
set -e

VERSION=${VERSION:-2.2.0}

# Automatically detect architecture
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
wget "$DOWNLOAD_URL" -O nerdctl.tgz

echo "Extracting..."
tar -xzf nerdctl.tgz

# After extraction, you will get binaries such as nerdctl, containerd, runc, etc.
# Generally, nerdctl is located in the current directory's nerdctl
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