---
categories:
- Interview
date: 2025-12-06 10:42:12
draft: false
tags:
- Database
title: SRE Interview Questions | Database
---

# mysql
## 1. How to troubleshoot a sudden slow MySQL query
### Check the query itself
- Review if the SQL query can be optimized, such as using appropriate indexes, avoiding full table scans, etc.
- Complex JOIN operations: Confirm if there are multiple large table joins or unnecessary complex operations.

### Check database performance
Slow query log: Enable and check the slow query log (slow_query_log). Review which queries have been running for a long time recently.

### Check system load
System resources: Check if there are bottlenecks in CPU, memory, disk IO, and network resources. Use tools like top or htop to monitor.
Disk IO: Check if disk read/write has become a bottleneck. Use tools like iostat or vmstat to view disk IO status.

### Check lock and concurrency issues
Lock status: Check if there are lock waiting or deadlock issues. Use the following SQL statements to view the current lock status:
If there are many threads in the "Locked" state, it may be necessary to further analyze the source of the locks and find solutions.

### Network latency
If connecting to MySQL remotely, confirm if the network connection is stable and if there is high latency.

# redis
## 1. Hotkey and large key issues
### Hotkey issues
- Hotkey: Refers to frequently accessed keys that may lead to decreased database performance.

Impact:
- CPU concentrated on a single Redis node
- QPS uneven, cluster load imbalance
- Latency spikes, request timeouts
- Triggering failover in nodes

Solutions
- Business layer sharding/bucketing: Split hot requests into multiple keys to improve concurrency capacity.
- Increase cache layer: Local cache + Redis secondary cache to reduce direct access to Redis.
- Use multi-key splitting to read pressure, breaking a hot large key into multiple sub-keys.
- Hotspot protection at the Redis Proxy layer, where the proxy layer can identify hotspots and perform degradation.
- Client-side local throttling + degradation

### Large key issues
- Large key: Refers to keys with very large values that occupy a large amount of memory space.

Impact:
- Slow during migration slots (CLUSTER ADDSLOTS/MIGRATE)
- May block the Redis main thread
- Trigger blocking during deletion (del O(n) operation)
- Overload network bandwidth
- Increase in read/write latency
- Slow failover recovery

Solutions
- Business layer splitting: Split large keys into multiple small keys, with each small key storing only a portion of the data.
- Pagination read: Do not use hgetall/smembers/zrange, use scan / segmented retrieval.
- Pre-limit the size of the value: Do key size limits on the service side.
- Avoid storing logs, messages, and long texts in Redis.

How to find large keys
- Redis's SCAN command
- redis-cli -h 127.0.0.1 -p 6379 —bigkeys
- Open-source tool Redis RDB Tools, analyze RDB files, and scan out Redis large keys.

# kafka
## 1. How to handle message backlog

### Causes of message backlog
- Producers produce a large number of messages to a Topic in a short period of time, and consumers cannot consume them in time.
- Consumers have insufficient consumption capacity (low consumer concurrency, long message processing time), leading to consumption efficiency lower than production efficiency.
- Consumer anomalies (such as consumer failures, consumer network anomalies, etc.) causing inability to consume messages.
- Topic partition settings are not reasonable, or new partitions are added without consumers consuming them.
- Topic frequent rebalancing leads to reduced consumption efficiency.

### Solutions
From the causes of message backlog, the message backlog problem can be handled from three aspects: consumer side, producer side, and service side.
- Consumer side
  - Increase the number of consumers according to actual business needs to ensure that the number of partitions/consumers is an integer, and it is recommended that the number of consumers and partitions be consistent.
  - Increase the consumption speed of consumers by optimizing consumer processing logic (reducing complex calculations, third-party interface calls, and read database operations), reducing consumption time.
  - Increase the number of messages pulled by consumers each time: Pull data/process time >= production speed.
- Producer side
  - Add a random suffix to the message Key when producing messages to balance the distribution of messages to different partitions.
- Service side
  - Reasonably set the number of partitions for the Topic, and increase the number of Topic partitions without affecting business processing efficiency.
  - When message backlog occurs on the service side, implement circuit breaking for producers or forward producers' messages to other Topics.