---
title: "SRE面试题汇总 | K8s"
date: 2025-12-06T18:15:30+08:00
draft: false
categories:
    - 面试
tags:
    - K8s
---

## 1.各模块如何与API Server通信
集群内的各个功能模块通过API Server将信息存入etcd，当需要获取和操作这些数据时，则通过API Server提供的REST接口（用GET、LIST或WATCH方法）来实现，从而实现各模块之间的信息交互。

Kubernetes中各模块通过标准的HTTP/HTTPS请求与API Server交互，通过认证和鉴权机制保证安全性，并利用Watch机制实现实时的资源状态监控与同步。

## 2.kubelet监控worker节点如何实现
```
Linux 内核
    ↓
cAdvisor 采集容器与节点指标
    ↓
kubelet 处理、聚合、判断节点状态
    ↓
apiserver + metrics server 汇总
    ↓
kubectl top / HPA / 调度器 决策
```

## 3.集群节点规模上千注意事项
官方文档https://kubernetes.io/zh-cn/docs/setup/best-practices/cluster-large/


## 4. kubeconfig存放内容
有关集群、用户、命名空间和身份验证机制的信息

## 5. kube-proxy 的作用
核心职责 维护 Service 的转发规则
kube-proxy 监听 API Server 中 Service、Endpoints/EndpointSlice 的变化，在节点上维护 iptables 或 IPVS 规则，实现 Service 到后端 Pod 的流量转发。

### 类型
- iptables：默认模式，使用 iptables 规则实现 Service 转发。
- IPVS：基于Linux 内核 IPVS 进行四层负载均衡，性能高，规则更新快。

## 6. scheduler调度流程
1. 监听与获取 (Listen & Get)
- Scheduler 监听 K8s API Server，发现未绑定到节点的 Pod
- 通过 Informer 机制，从本地缓存获取 Pod 和 Node 的实时信息，提高效率
2. 预选阶段 (Predicates/Filter)
- 快速过滤掉不满足条件的节点，减少后续计算量
- 节点资源（CPU, Memory）、Node Selector/Affinity/Anti-Affinity、Taints/Tolerations、Pod 预留等。得到一个通过所有过滤器的“候选节点”列表。
3. 优选阶段 (Priority)
- 打分：为通过预选的节点打分，评估其“好坏”。
- 节点资源利用率、负载均衡、拓扑位置（如优先同一机架/区域）。
结果: 得到一个按分数降序排列的节点列表
4. 绑定阶段 (Bind)
- 选择得分最高的节点
- 将选择结果写入本地缓存 (Scheduler Cache)，记录资源占用，并尝试预留资源。
- 异步调用 API Server，更新 Pod 的 spec.nodeName，将 Pod 绑定到选定节点。
-  Kubelet 监听到 Pod 绑定事件后，开始创建容器

## 7. POD 的启动流程
- 用户通过kubectl或其他工具提交pod的yaml配置到API Server
- API Server 收到请求后，将配置存储到etcd中
- Scheduler 根据调度策略，将 Pod 绑定到合适的节点
- Kubelet 监听到 Pod 绑定事件后，开始创建容器
  - 拉取镜像
  - 创建sandbox，sandbox中所有容器共享网络和存储命名空间
  - 调用容器运行时创建pod中的容器
  - 如果有init容器，kubelet先于应用容器启动他们
  - aws-node 创建pod网卡，分配IP地址
- 容器启动后，Kubelet 向 API Server 发送状态更新
- API Server 收到更新后，将状态存储到etcd中
- 用户通过kubectl或其他工具查询 Pod 状态时，API Server 从etcd中获取最新状态并返回

## 8. pod dns 解析失败排查
1. 检查 Pod 内部和配置
- kubectl exec -it <pod> -- nslookup kubernetes.default  集群内部 DNS 故障
- kubectl exec -it <pod> -- curl https://www.google.com 上游 DNS 或 CoreDNS 配置问题
- 检查 DNS Policy：查看 Pod YAML，确保 dnsPolicy (如 ClusterFirst) 配置正确. 
Default: Pod 从运行所在的节点继承域名解析配置
ClusterFirst: Pod 先从集群内部 DNS 解析，失败后再使用节点 DNS 配置

2. 检查coredns
- 检查core dns 负载
- 检查coredns configmap forward

3. 排查 kube-proxy
DNS 的流量是 Pod → kube-proxy → CoreDNS Pod
4. 检查 CNI 网络插件
5. 是否使用了 Istio / Linkerd / Envoy sidecar

## 9. Pod的常见调度方式
1. 默认调度器（Default Scheduler）
2. 节点选择器（Node Selector）
3. 亲和性和反亲和性（Affinity and Anti-Affinity）
4. 污点和容忍度（Taints and Tolerations）
5. 资源请求和限制（Resource Requests and Limits）
6. Pod 拓扑调度（Pod Topology Spread）： 不同节点/机架均匀分布
7. 抢占调度（Preemption）

## 10. Pause容器的用途
Pause 容器唯一的作用是 保证即使 Pod 中没有任何容器运行也不会被删除，因为这时候还有 Pause 容器在运行。
- 网络命名空间隔离
- 进程隔离
- 资源隔离
- 生命周期管理

## 11. pod健康检查失败可能的原因和排查思路
- 探针配置问题
- 应用未启动/响应慢：超出initialDelaySeconds，进程退出 (CrashLoopBackOff)
- 资源限制：CPU/内存不足，导致Kubelet无法正常运行检查
- 网络问题：容器无法访问外部服务，如DNS解析失败
- 依赖不可用： 数据库、缓存等依赖服务未就绪
- 数据库、缓存等依赖服务未就绪

排查思路
- kubectl describe pod
- kubectl logs
- 检查健康检查配置
- 进入容器内部排查
  - 使用curl, wget测试HTTP探针路径。
  - netstat -tulnp或ss -tulnp确认端口是否监听
- 检查资源与节点

## 12. pod之间访问不通怎么排查

## 13. pod几种常见状态
Pod Phase

- Running 
- Succeeded Job 完成、CronJob 完成
- Failed 程序崩溃、容器启动失败
- Pending 资源不足、NodeSelector 无匹配、拉镜像慢
- Unknown kubelet 无法上报状态，节点掉线、网络中断

创建/调度相关
- ContainerCreating 容器正在创建容器，拉取镜像
- PodInitializing 容器正在初始化，执行 init 容器
- ImagePullBackOff 拉镜像失败（认证问题、镜像不存在）
- ErrImagePull 同上，比 BackOff 更早期

运行中异常
- CrashLoopBackOff 容器崩溃后，kubelet 会根据 backoff 策略（默认 10s 后重试）重启容器
- OOMKilled 容器内存超出限制，被 kubelet 强制kill
- BackOff 多次失败后进入退避（如 init 容器失败）
- CrashLoopBackOff 主容器不断崩溃重启
- CreateContainerConfigError 容器创建配置错误（如挂载卷不存在）
- Error 容器非0退出（但不一定重启策略触发失败）


退出/终止
- Terminating 容器正在终止（如删除 pod）
- Completed 容器正常退出（如主容器退出）
- Failed 容器非0退出，且重启策略为 Never