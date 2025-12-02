---
title: "字节国际电商"
date: 2025-12-02T15:19:21+08:00
draft: false
categories:
    - 面试
---

## 一轮面试
### k8s 中几种探针方式
- livenessProbe 捕获死锁。决定容器何时重启
- readinessProbe 检查容器是否准备好接收流量。
- startupProbe 检查容器内服务是否启动完成， 启动探针可以用于对慢启动容器进行存活性检测，避免它们在启动运行之前就被 kubelet 杀掉。
  
### 跨region 双写、三写数据一致性问题


### pod 资源节点抢占解决方案

kubelet 开启节点 --cpu-manager-policy=static

### k8s 服务中扩缩怎样实现

HPA 自动根据 CPU 利用率或自定义指标来调整 Deployment 的副本数。

### 一次troubleshooting

### 报警架构如何做的

### 当前工作中的存在的痛点

### 你会关注业务哪些指标

### 广告竞价返回的数据格式

### 一道力扣题 复原IP地址

