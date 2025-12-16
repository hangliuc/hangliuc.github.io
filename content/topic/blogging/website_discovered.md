---
title: "Hugo ｜ 如何让搜索引擎检索到博客"
date: 2025-12-15T19:45:07+08:00
draft: false
categories:
    - 博客
---
部署完博客后，需要让搜索引擎检索到博客。

## google
### 获取Measurement ID
[google 分析官方网站](https://analytics.google.com/analytics/web/provision/#/provision)
在 google 分析中，每个网站都有一个唯一的 Measurement ID，格式为 `G-XXXXXXXXXX`。这个 ID 用于将网站的访问数据发送到 google 分析。

在hugo.yaml 中添加如下配置：

如果你是yaml 格式，注意要是最顶级的配置
```yaml
googleAnalytics: G-xxxx # <--- 换成你的 Measurement ID
```

### 提交siteMap
siteMap 是一个 xml 文件，用于告诉搜索引擎你的网站有哪些页面。

Hugo 会在生成和部署网站时在 public 文件夹根目录下自动生成 sitemap.xml 文件

登录[谷歌搜索控制台](https://search.google.com/search-console)。在验证所有权的选项中选择 “Google Analytics”，输入你的 Measurement ID 即可验证所有权。

下面就是已经成功提交的截图
![google 搜索控制台验证所有权](img/blog/google_search_console.png)

### 如何验证文章已经被Google 收录
对于一个新站，Google 可能需要 几天甚至几周 才能把所有页面全部收录

#### Google Search Console 验证
直接在顶部的搜索框查询，输入你的文章链接，即可验证是否被收录。
![google 搜索控制台验证所有权](img/blog/gcs01.png)

也可以直接点击请求编入索引，请求 Google 收录你的文章。

#### google 搜索验证
![google 搜索控制台验证所有权](img/blog/gcs02.png)


tips:
- 验证收录可能需要 几天甚至几周 才能完成。
- 文章的标题尽可能增加关键词密度，更加吸晴，让用户有点击的欲望。


## refs
https://hyrtee.github.io/2023/start-blog/#refs