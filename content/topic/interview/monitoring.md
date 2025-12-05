---
title: "Monitoring"
date: 2025-12-05T13:38:56+08:00
draft: false
categories:
    - 面试
tags:
    - 监控
---

## 1.监控指标类型及应用场景
1、 计数器（Counter）：用于记录事件的数量，例如请求次数、错误次数等。
- 特点：单调递增，只增不减，重启时被设置为0
- 场景：qps、error、已经完成的任务数等

2、 计量器（Gauge）：用于记录当前的数值，例如内存使用量、CPU 利用率等。
- 特点：可增可减，可以任意变化的指标
- 场景：cpu、mem、disk、network等


Histogram和Summary主用用于计算分位数，统计和分析样本的分布情况。

3、 直方图（Histogram）：用于记录事件的分布情况，Prometheus 服务端通过 bucket 计算分位数。
- 特点：要提前定义 bucket（如 10ms、50ms、100ms…），用于将样本值分桶。可以聚合跨实例的全局分位数（Summary 做不到）
- 场景：业务接口延迟监控，p95、p99
```sql
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

4、 摘要（Summary）：
- 特点：不需要 bucket，代码内自动维护 quantile。无法跨实例计算全局 p99 
如果你有 10 个 pod，各自暴露 p99，那么 Prometheus 不能再算“整个服务的 p99”
- 场景：每个实例都独立的统计需求

Summary 的分位数是在客户端（应用）本地计算的，Prometheus 只需存储最终的 p95、p99 数值。但是不能聚合跨实例的全局分位数。 
Histogram在服务端计算分位数，Histogram 能够将多个实例的数据聚合在一起，得出整个服务的全局分位数，是k8s生产环境最常用的方式。

## 2. 黄金指标
- 延迟（Latency）
- qps
- 错误率（Error Rate）
- 饱和度（Saturation）