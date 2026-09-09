---
title: "SRE面试题汇总 | Monitoring"
image: /img/cover/monitoring_interview_cover.png
date: 2025-12-05T13:38:56+08:00
draft: false
categories:
    - 面试
tags:
    - 监控
---

## 监控指标类型及应用场景

Prometheus 中常见的指标类型包括 Counter、Gauge、Histogram 和 Summary。选择指标类型时，要结合指标是否单调递增、是否需要聚合，以及是否需要计算分位数来判断。

### Counter：计数器

用于记录请求次数、错误次数、完成任务数等事件数量。

- 特点：在单个进程生命周期内单调递增，只能增加不能减少；进程重启后通常会从 0 重新开始，Prometheus 的 `rate`、`increase` 等函数可以处理这类 Counter 重置。
- 场景：请求总数、错误总数、已完成任务总数。

### Gauge：计量器

用于记录某一时刻的数值，例如内存使用量、CPU 使用率、磁盘空间和队列长度。

- 特点：可以增加，也可以减少，数值会随时间上下变化。
- 场景：CPU、内存、磁盘、网络流量、在线人数、队列长度。

### Histogram：直方图

用于记录请求延迟、响应大小等样本的分布情况。应用需要预先定义 bucket，例如 10ms、50ms、100ms 和 500ms，Prometheus 根据 bucket 在服务端计算分位数。

- 可以聚合多个实例的 bucket，计算整个服务的全局 p95、p99。
- 适合业务接口延迟、任务耗时和响应大小等分布监控。

```promql
histogram_quantile(
  0.99,
  sum by (le) (rate(http_request_duration_seconds_bucket[5m]))
)
```

### Summary：摘要

Summary 不需要预先定义 bucket，而是在客户端或应用进程内维护 quantile，并将计算结果暴露给 Prometheus。

- 适合每个实例独立统计的场景。
- 不适合聚合跨实例的全局分位数。例如 10 个 Pod 各自暴露 p99，Prometheus 不能直接对这 10 个 p99 再计算出整个服务的准确 p99。
- Summary 的 `_sum` 和 `_count` 可以参与聚合计算平均值，但分位数本身通常不能直接聚合。

生产环境中，如果需要计算整个服务的全局分位数，通常优先选择 Histogram；如果只关心单个实例的本地分布，Summary 也可以使用。

## 黄金指标

常见的四类黄金指标是 Latency、Traffic、Errors 和 Saturation：

- **延迟（Latency）**：请求从开始到结束耗费的时间，通常关注 p50、p95、p99。

  ```promql
  histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))
  ```

- **流量（Traffic）**：系统承载的请求量或业务量，常用 QPS 表示。

  ```promql
  sum(rate(http_requests_total[5m])) by (handler)
  ```

- **错误率（Error Rate）**：失败请求占总请求的比例。

  ```promql
  sum(rate(http_requests_total{status=~"5.."}[5m]))
  /
  sum(rate(http_requests_total[5m]))
  ```

- **饱和度（Saturation）**：资源接近容量上限的程度，例如 CPU、内存、连接池、线程池和队列的使用情况。具体 PromQL 要根据采集的指标定义，不能只用一个通用表达式代替所有资源。




## rate 与 irate 的区别

- `rate`：根据指定时间窗口内的多个样本计算平均每秒增长率，结果更平滑，适合趋势分析和告警。
- `irate`：只使用时间窗口内最后两个样本计算瞬时增长率，对短期突发变化非常敏感，适合实时看板或快速观察突发流量。

告警通常优先使用 `rate`，并结合较短的 `for` 持续时间减少误报。`irate` 并不是绝对不能用于告警，但需要确认采样间隔、窗口长度和业务波动都适合，否则容易因单个采样点抖动而频繁触发。

## 如何对采集指标进行过滤？

在 Prometheus 或 vmagent 中，常见的过滤位置如下：

```text
Exporter / Kubernetes / AWS 云监控
          │
          ▼
       vmagent
          │
          ├─ relabel_configs
          │      抓取前，处理 Target 标签和目标地址
          │
          ├─ 发起 HTTP 请求抓取 /metrics
          │
          ├─ metric_relabel_configs
          │      抓取后，处理每条时序样本
          │
          ├─ write_relabel_configs
          │      Remote Write 发送前，过滤即将写出的时序
          │
          ▼
       vminsert
          │
          ▼
       vmstorage
```

- **`relabel_configs`**：发生在抓取前，常用于修改目标标签、替换地址、按环境过滤 Target。
- **`metric_relabel_configs`**：发生在抓取后，作用于每条指标，适合丢弃不需要写入的高基数指标或标签。
- **`write_relabel_configs`**：发生在 Remote Write 发送前，可按目标远程存储过滤时序。

过滤规则要谨慎使用，尤其要关注高基数标签、误删核心指标以及规则变更后的数据缺口。

## Prometheus 服务发现方式

Service Discovery（SD）用于自动发现需要抓取的 Target。常见方式包括静态配置、文件服务发现、Kubernetes SD、Consul SD 和云厂商 SD。

### 静态配置

适合 Target 数量少、地址变化不频繁的场景：

```yaml
scrape_configs:
  - job_name: node
    static_configs:
      - targets:
          - 10.0.0.1:9100
          - 10.0.0.2:9100
```

### File SD：文件服务发现

由外部系统生成 JSON 或 YAML 文件，Prometheus 定期读取文件中的 Target：

```yaml
scrape_configs:
  - job_name: node
    file_sd_configs:
      - files:
          - /etc/prometheus/*.json
```

### Kubernetes SD

Prometheus 通过 Kubernetes API 发现 Pod、Service、Node 等对象，再配合 relabel 选择需要抓取的目标：

```yaml
scrape_configs:
  - job_name: kubernetes-pods
    honor_labels: true
    kubernetes_sd_configs:
      - role: pod
```

实际使用时还需要配置 Kubernetes API 访问权限，并通过 `relabel_configs` 过滤 Namespace、Annotation 或 Label。

### Consul SD

服务注册到 Consul 后，Prometheus 根据服务标签和健康状态自动发现目标：

```yaml
scrape_configs:
  - job_name: consul-services
    consul_sd_configs:
      - server: 10.151.91.180:8500
        datacenter: dc1
```

### AWS EC2 SD

在 AWS 环境中可以通过 EC2 服务发现获取实例信息，通常使用实例角色提供权限，避免把 Access Key 直接写入配置文件：

```yaml
scrape_configs:
  - job_name: ec2-node
    ec2_sd_configs:
      - region: ap-southeast-1
        port: 9100
```

## Target 监控不到如何排查？

先从 Prometheus 的 `/targets` 页面或 API 查看 Target 处于哪一种状态：

```shell
curl http://prometheus:9090/api/v1/targets
```


### Target 不存在

- 检查 `static_configs`、File SD 文件和服务发现配置是否生效。
- 检查 Prometheus 或 vmagent 是否有权限访问 Kubernetes API、Consul 或云厂商 API。
- 检查 `relabel_configs` 是否误删了 Target，尤其是 `action: drop` 和 `action: keep`。
- 如果使用 File SD，确认文件路径、JSON/YAML 格式和文件权限正确。

### Target 存在但状态为 DOWN

- 从 Prometheus 或 vmagent 所在的 Pod/主机执行 `curl`，确认目标地址和端口可达。
- 检查 `metrics_path`、`scheme`、端口、HTTP 认证和 TLS 证书配置。
- 检查安全组、防火墙、NetworkPolicy、Service 和 Endpoints 是否放行流量。
- 查看 Target 的 `Last Error`，区分连接拒绝、连接超时、DNS 失败、TLS 失败和返回非 2xx。

### Target UP 但查询不到指标

- 直接访问目标的 `/metrics`，确认指标确实被应用或 Exporter 暴露。
- 检查 `metric_relabel_configs` 或 Remote Write 过滤规则是否丢弃了指标。
- 检查 PromQL 中的指标名、Label、时间范围和数据源是否正确。
- 检查 Grafana 数据源、远程存储写入链路和数据保留策略。

排障时要先确认“Target 是否存在”，再确认“是否能抓取”，最后确认“指标是否被写入和查询”，不要一开始就只看 Grafana 面板。
