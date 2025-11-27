---
title: "Todo"
date: 2025-11-27T11:04:45+08:00
draft: false
---

## Hugo 目录结构
content/: 存放你的 Markdown 文章（数据库）。

layouts/ & themes/: 存放前端代码（HTML/CSS 模版）。

static/: 存放图片、CNAME 文件等静态资源。

hugo.toml (或 .yaml/.json): 整个站点的配置文件（相当于 k8s 的 configmap）

## 内容相关
- [ ] 在github、CSDN、yuque、公众号通过统一的目录结构发布内容，目录结构如下：
```
- 运维
    - Mysql
    - Redis
    - Kafka
    - ansible
    - k8s
    - aws
    - Linux
    - Docker
    - prometheus
    - Terraform

- 编程
    - Python
    - Shell
    - Go
    - 数据结构
    - 算法

- 专题
  - 博客相关
  - 面试相关
  - Liunx 性能优化
  - Mysql 实战

```
尽量不更新一些基础的知识，通过浏览器搜索即可，增强搜索知识的能力。重点记录一些在生产环境中遇到的问题和解决方法。