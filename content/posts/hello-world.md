---
title: "Hello World"
date: 2023-11-26T10:00:00+08:00
draft: false
---

这是我的第一篇 Hugo 博客！

## 为什么选择 Hugo？
作为 SRE，我喜欢静态二进制文件的简单和纯粹。

## Hugo 目录结构
content/: 存放你的 Markdown 文章（数据库）。

layouts/ & themes/: 存放前端代码（HTML/CSS 模版）。

static/: 存放图片、CNAME 文件等静态资源。

hugo.toml (或 .yaml/.json): 整个站点的配置文件（相当于 k8s 的 configmap）