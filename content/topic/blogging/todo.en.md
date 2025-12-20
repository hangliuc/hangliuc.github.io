---
categories:
- Blog
date: 2025-11-27 03:04:45
draft: false
title: Hugo | To-Do List
weight: 1
---

## 📝 Blog To-Do List
### 🔥 P0
- [ ] Make the blog indexable by search engines like Google, Baidu, etc.
    - [x] Submit Google sitemap
    - [ ] Submit Baidu sitemap; a record number is required to increase the submission frequency when submitting Baidu sitemap
- [ ] Optimize website access speed
    - [x] Enable BBR congestion control net.ipv4.tcp_congestion_control = bbr


### 🛠 P1
- [ ] Develop an agent that simultaneously publishes to yuque, csdn, weichat
   - yuque API token requires payment
   - csdn currently has not found a suitable API
- [ ] Beautify the website's right sidebar
     Add excellent articles, and count based on access volume
- [ ] Create a separate homepage, you can refer to https://www.shaohantian.com/
- [ ] Optimize SEO search result snippets to improve the aesthetics of search results
- [ ] Write some introductions about myself
- [ ] Develop a management platform
- [ ] Add a list of commonly used tools


### ✅Archived - Launched Features
- [x] Add comment functionality
  - [x] Migrate comment functionality to waline
  - [x] Notify wechat, email, and other channels for comments
- [x] Improve keyword search functionality
- [x] Add article word count
- [x] Add an English version of the site, implementing automatic translation from Chinese to English
  - Script calls a large model to automatically translate Chinese articles into English
  - Script translation adds intelligent incremental updates (implementation logic: compare file modification time)
  - Page header website statistics information adapts to the English version
  - Article top word count and reading volume statistics adapt to the English version
  - The left sidebar switch button changes from a dropdown box to direct switching
- [x] Beautify the browser top icon
- [x] Add "Back to Top" functionality to the homepage and articles
- [x] Deploy the website on the server
    The server is not in China, so it can be备案
    Domain: hangops.top, first year ¥14, renewal ¥32
- [x] Deploy monitoring system
    - [x] Deploy Prometheus
    - [x] Deploy Grafana(https://monitor.hangops.top/)
- [x] Add website access statistics
    - [x] Count website visits
    - [x] Count article visits
- [x] Backup blog mysql database to cos storage bucket



## Content Related
The directory structure is as follows:
```
- Operations
    - Mysql
    - Redis
    - Kafka
    - ansible
    - k8s
    - aws
    - Linux
    - Docker
    - Prometheus
    - Terraform

- Programming
    - Python
    - Shell
    - Go
    - Data Structures
    - Algorithms

- Special Topics
  - Blog Related
  - Interview Related
  - Linux Performance Optimization
  - Mysql Practical Application
```