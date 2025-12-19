---
categories:
- Blog
date: 2025-11-27 03:04:45
draft: false
title: Hugo | To-Do List
weight: 1
---

## To-Do List
### Aesthetics and User Experience Optimization
- [x] Improve comment feature
- [ ] Beautify the website's right sidebar
    Add excellent articles, and count based on the number of visits
- [x] Beautify the browser's top icon
- [ ] Create a separate homepage, for reference: https://www.shaohantian.com/
- [ ] Optimize SEO search result snippets for better aesthetics


### Feature Development and Content Expansion
- [x] Improve search functionality
- [x] Add word count for articles
- [x] Add an English version of the site with automatic translation from Chinese to English
  - Script calls a large model to automatically translate Chinese articles to English
  - Header website statistics information adapted for the English version
  - Article top word count and reading count statistics adapted for the English version
  - Left sidebar switch button changed from dropdown to direct switch
  - Script translation adds intelligent incremental updates (logic: compare file modification time)
- [ ] Develop an agent to simultaneously publish to yuque, csdn, weichat
   - Currently, the yuque API token requires a fee
- [x] Write a brief introduction about myself
- [x] Add "Back to Top" functionality
- [x] Migrate comment feature to waline
  - [x] Comment notifications to wechat, email
- [x] Make the blog searchable on google, baidu
   Baidu requires a record number for sitemap submission, so it will not be added for now.
- [ ] Backup blog database
- [ ] Develop a management platform


### Deployment and Monitoring
- [x] Deploy the website on the server

    The server is not in China, so there is no need to file a record for the first year

    First Year  Renewal
    hangops.top ¥14 ¥32

- [x] Deploy monitoring system
    - [x] Deploy Prometheus
    - [x] Deploy Grafana

https://monitor.hangops.top/
- [x] Add website visit statistics
    - [x] Count website visits
    - [x] Count article visits


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
  - Blog-related
  - Interview-related
  - Linux Performance Optimization
  - Mysql Practical Application

```
Try not to update basic knowledge, which can be searched through the browser to enhance search knowledge skills. Focus on recording problems encountered and solutions in production environments.