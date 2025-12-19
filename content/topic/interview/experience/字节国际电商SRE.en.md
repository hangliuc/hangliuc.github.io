---
categories:
- Interview
date: 2025-12-02 07:19:21
draft: false
title: Interview | ByteDance International E-commerce
---

## First Round Interview
### Several Probe Methods in k8s
- `livenessProbe` detects deadlocks and determines when a container should be restarted.
- `readinessProbe` checks if the container is ready to receive traffic.
- `startupProbe` checks if the service inside the container has started up. The startup probe can be used for slow-starting containers to perform liveness checks, preventing them from being killed by kubelet before they start running.

### Data Consistency Issues with Dual-Writing or Triple-Writing Across Regions

### Pod Resource Node Preemption Solution

Enable node options in kubelet: `--cpu-manager-policy=static`

### How to Implement Scaling in k8s Services

HPA (Horizontal Pod Autoscaler) automatically adjusts the number of replicas of a Deployment based on CPU utilization or custom metrics.

### Troubleshooting Experience

### How to Design an Alert Architecture

### Pain Points in Current Work

### Which Business Metrics Would You Focus On

### Data Format of Ad Auction Returns

### A LeetCode Question: Restore IP Addresses