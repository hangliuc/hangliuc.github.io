---
categories:
- Blog
date: 2025-11-27 07:16:29
draft: false
title: Hugo | Basic Planning and Usage Method
---

## Hugo Directory Structure
content/: Stores your Markdown articles (database).

layouts/ & themes/: Stores frontend code (HTML/CSS templates).

static/: Stores images, CNAME files, and other static resources.

hugo.toml (or .yaml/.json): The configuration file for the entire site (similar to k8s's configmap)

## Comment System
Giscus Comment System
https://giscus.app/zh-CN

hugo.yaml
```yaml
params:
    # ... Other configurations ...

    comments:
        enabled: true
        provider: giscus  # <--- Change the default disqus to giscus

        giscus:
            repo: hangliuc/blog-hugo  # <--- Replace with your "username/repository"
            repoID: "R_kgD..."        # <--- Fill in the data-repo-id obtained in the second step
            category: "Announcements" # <--- The category name you choose
            categoryID: "DIC_kw..."   # <--- Fill in the data-category-id obtained in the second step
            mapping: pathname
            lightTheme: light
            darkTheme: dark_dimmed
            reactionsEnabled: 1
            emitMetadata: 0
```

In addition, you need to authorize the Giscus comment system on GitHub.
Reference link: https://giscus.app/zh-CN

## Categories and Tags

Categories (Categories): Like folders, they are usually tree-like and exclusive. An article usually belongs to 1-2 categories (e.g., "Operations", "Containerization").

Tags (Tags): Like sticky notes, they are flat and descriptive. An article can have multiple tags (e.g., "Docker", "Networking", "Troubleshooting", "Linux").

## Some Useful Links

Icon download website: https://tabler.io/icons

## Some Excellent Websites Built with hugo-theme-stack

https://liuhouliang.com/categories/web/


https://blog.reincarnatey.net/

https://zfj1441.com/archives/

https://hyrtee.github.io/2023/start-blog/#%E8%AF%84%E8%AE%BA


https://www.shaohantian.com/