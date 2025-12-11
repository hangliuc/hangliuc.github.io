---
title: "博客 | Hugo 基础规划和使用方法"
date: 2025-11-27T15:16:29+08:00
draft: false
categories:
    - 博客
---


## Hugo 目录结构
content/: 存放你的 Markdown 文章（数据库）。

layouts/ & themes/: 存放前端代码（HTML/CSS 模版）。

static/: 存放图片、CNAME 文件等静态资源。

hugo.toml (或 .yaml/.json): 整个站点的配置文件（相当于 k8s 的 configmap）

## 评论系统
Giscus 评论系统
https://giscus.app/zh-CN

hugo.yaml
```yaml
params:
    # ... 其他配置 ...

    comments:
        enabled: true
        provider: giscus  # <--- 将默认的 disqus 改为 giscus

        giscus:
            repo: hangliuc/blog-hugo  # <--- 换成你的 "用户名/仓库名"
            repoID: "R_kgD..."        # <--- 填入第二步获取的 data-repo-id
            category: "Announcements" # <--- 你选择的分类名
            categoryID: "DIC_kw..."   # <--- 填入第二步获取的 data-category-id
            mapping: pathname
            lightTheme: light
            darkTheme: dark_dimmed
            reactionsEnabled: 1
            emitMetadata: 0
```

除此之外需要去GitHub 授权 Giscus 评论系统
参考链接 https://giscus.app/zh-CN

## 分类和标签

Categories (分类)：像文件夹一样，通常是树状、排他性的。一篇文章通常属于 1-2 个分类（例如“运维”、“容器化”）。

Tags (标签)：像便利贴一样，是扁平、描述性的。一篇文章可以有多个标签（例如“Docker”、“网络”、“Troubleshooting”、“Linux”）。

## 一些可用链接

图标下载网站 https://tabler.io/icons

## 一些使用 hugo-theme-stack 搭建的优秀网站
https://liuhouliang.com/categories/web/

https://munlelee.github.io/

https://blog.reincarnatey.net/

https://zfj1441.com/archives/

https://hyrtee.github.io/2023/start-blog/#%E8%AF%84%E8%AE%BA