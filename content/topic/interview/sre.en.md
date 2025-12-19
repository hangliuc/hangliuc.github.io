---
categories:
- Interview
date: 2025-12-04 10:06:35
draft: false
tags:
- sre
title: SRE Interview Questions Summary | SRE
---

## 1. SLA, SLO, SLI
SLI: Service Level Indicator (percentage of normal response counts)

SLO: Service Level Objective (99%, 99.999%, 99.99999%)
Must be tied to time

SLA: Service Level Agreement (the specific implementation of SLO)


SLA is the external commitment to the customer, SLO is the internal goal set by the company to achieve the commitment, and SLI is the indicator used to measure the actual service performance.

## 2. MTTR
MTTR: Mean Time to Repair (Average Time to Repair)

MTTR = Total Time to Repair ÷ Number of Faults

### How to Reduce MTTR?

### Monitoring
- Improve the monitoring and alerting system
  - Business metric monitoring
  - System metric monitoring
- Alert Noise Reduction
  - Alert Grading: p1, p2, p3
  - Alert Escalation: When an alert level is P2 and has not been handled (not closed, not suppressed, etc.) within 1 hour, it will automatically escalate to p1
  - Alert Interval: The minimum interval for the same alert to be sent by default is 15m
  - Alert Flood: Set appropriate alert strategies to avoid too many alerts and alert loss

### Fast Location
- Standardized troubleshooting SOP
  - How to check when CPU and memory are soaring
  - How to check when ELB 5xx occurs
  - How to check when Pod CrashLoop occurs
- Automatically capture on-site information
  - C++ core dump
- Unified logging platform
  - ELK / Loki
- Full-link tracking

### Fast Problem Resolution
- Gray release / Canary release
- Configuration center (apollo) + dynamic traffic splitting (like a switch to turn off a module)
- Auto-scaling (auto-scaling based on business traffic, HPA)
- Scripted repair
  - One-click restart
  - One-click clear DNS cache
  - ...

### High Availability Deployment
- High availability
- Multi-AZ deployment
- Automatic failover


### Continuous Drills & Reliability Testing
- Chaos engineering (pre-drill faults)
- Add missing monitoring points
- ...