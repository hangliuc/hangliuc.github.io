---
title: "Hugo ｜ to do list"
date: 2025-11-27T11:04:45+08:00
draft: false
categories:
    - 博客
weight: 1
---

## 📝 博客待办清单
### 🔥 P0 
- [ ] 让博客可以在google、百度等搜索引擎中被收录
    - [x] 提交 google sitemap
    - [ ] 提交百度 sitemap,百度提交sitemap时需要备案号才能增加提交次数
- [ ] 优化网站访问速度
    - [x]开启 BBR 拥塞控制 net.ipv4.tcp_congestion_control = bbr


### 🛠 p1
- [ ] 开发agent 同时发布上传yuque、csdn、weichat
   - yuque api token 需要付费
   - csdn 目前没有找到合适的api
- [ ] 美化网站右侧边栏
     添加优秀文章,根据访问量去统计
- [ ] 单独制作首页，可以参考https://www.shaohantian.com/
- [ ] SEO 搜索结果片段优化，提高搜索结果的美观性 
- [ ] 写关于我的一些说明
- [ ] 开发管理平台
- [ ] 增加常用工具列表

### ✅Archived - 已上线功能
- [x] 增加评论功能
  - [x] 评论功能迁移到waline
  - [x] 评论通知 wechat、email 等渠道
- [x] 完善关键字搜索功能
- [x] 添加文章字数统计
- [x] 添加英文站，实现中文到英文的自动翻译
  - 脚本调用大模型自动翻译中文文章为英文
  - 脚本翻译时添加智能增量(实现逻辑：比较文件的修改时间)
  - 页眉网站统计信息适配英文版
  - 文章顶部字数统计、阅读量统计适配英文版
  - 左侧边栏切换按钮由下拉框改为直接切换
- [x] 美化浏览器顶层图标
- [x] 首页和文章添加"返回顶部"功能
- [x] 服务器部署网站
    服务器不在国内可以先不备案
    域名：hangops.top，首年 ¥14，续费 ¥32
- [x] 部署监控系统
    - [x] 部署prometheus
    - [x] 部署grafana(https://monitor.hangops.top/)
- [x] 添加网站访问统计
    - [x] 统计网站访问量
    - [x] 统计文章访问量
- [x] 备份blog mysql 数据库到cos 存储桶



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
