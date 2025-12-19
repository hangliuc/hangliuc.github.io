---
categories:
- Interview
date: 2025-12-05 05:38:56
draft: false
tags:
- Surveillance
title: SRE Interview Questions Summary | Monitoring
---

## 1. Types of Monitoring Metrics and Application Scenarios
1. Counter: Used to record the number of events, such as the number of requests, number of errors, etc.
   - Characteristics: Monotonically increasing, only increases, reset to 0 upon restart
   - Scenarios: qps, error, number of completed tasks, etc.

2. Gauge: Used to record current values, such as memory usage, CPU utilization, etc.
   - Characteristics: Can increase or decrease, a metric that can change arbitrarily
   - Scenarios: cpu, mem, disk, network, etc.

Histogram and Summary are mainly used for calculating quantiles and analyzing the distribution of samples.

3. Histogram: Used to record the distribution of events, with Prometheus server calculating quantiles through buckets.
   - Characteristics: Buckets (such as 10ms, 50ms, 100ms, etc.) need to be predefined to bucket sample values. Can aggregate global quantiles across instances (Summary cannot do this)
   - Scenarios: Monitoring business interface latency, p95, p99
   ```sql
   histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
   ```

4. Summary:
   - Characteristics: No need for buckets, quantiles are automatically maintained in the code. Cannot calculate global p99 across instances
   If you have 10 pods, each exposing p99, then Prometheus can no longer calculate the "p99 of the entire service"
   - Scenarios: Independent statistical needs for each instance

The quantiles of Summary are calculated on the client (application) locally. Prometheus only needs to store the final p95, p99 values. However, it cannot aggregate global quantiles across instances.
Histogram calculates quantiles on the server, and Histogram can aggregate data from multiple instances to determine the global quantiles of the entire service, which is the most commonly used method in k8s production environments.

## 2. Golden Metrics
- Latency
- QPS
- Error Rate
- Saturation