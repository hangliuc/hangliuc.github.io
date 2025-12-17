---
title: "Hugo ｜ to do list"
date: 2025-11-27T11:04:45+08:00
draft: false
categories:
    - 博客
weight: 1
---
## 待办事项
### 美化与用户体验优化
- [x] 完善评论功能
- [ ] 美化网站右侧边栏
    添加优秀文章,根据访问量去统计
- [x] 美化浏览器顶层图标
- [ ] 单独制作首页，可以参考https://www.shaohantian.com/
- [ ] SEO 搜索结果片段优化，提高搜索结果的美观性


### 功能开发与内容扩展
- [x] 完善搜索功能
- [x] 添加文章字数统计
- [ ] 添加自动化英文版本

      自动将中文文章翻译成英文，不用手动发布文章
- [ ] 开发agent 同时发布上传yuque、csdn、weichat

      目前yuque api token 需要付费
- [x] 写关于我的一些说明
- [x] 添加“返回顶部”功能
- [x] 评论功能迁移到waline
- [x] 让博客在google、百度 中被搜索
   百度提交sitemap时需要备案号，这里先不添加。
- [ ]备份blog 数据库
- [ ] 开发管理平台

### 部署与监控
- [x] 服务器部署网站

    服务器不在国内可以先不备案

    首年  续费
    hangops.top ¥14 ¥32

- [x] 部署监控系统
    - [x] 部署prometheus
    - [x] 部署grafana

https://monitor.hangops.top/
- [x] 添加网站访问统计
    - [x] 统计网站访问量
    - [x] 统计文章访问量

## 内容相关
目录结构如下：
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

