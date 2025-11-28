---
title: "Hugo 基础规划和使用方法"
date: 2025-11-27T15:16:29+08:00
draft: false
categories:
    - 专题
tags:
    - blog
---


## Hugo 目录结构
content/: 存放你的 Markdown 文章（数据库）。

layouts/ & themes/: 存放前端代码（HTML/CSS 模版）。

static/: 存放图片、CNAME 文件等静态资源。

hugo.toml (或 .yaml/.json): 整个站点的配置文件（相当于 k8s 的 configmap）


## 图标下载网站

https://tabler.io/icons

## 分类和标签

Categories (分类)：像文件夹一样，通常是树状、排他性的。一篇文章通常属于 1-2 个分类（例如“运维”、“容器化”）。

Tags (标签)：像便利贴一样，是扁平、描述性的。一篇文章可以有多个标签（例如“Docker”、“网络”、“Troubleshooting”、“Linux”）。