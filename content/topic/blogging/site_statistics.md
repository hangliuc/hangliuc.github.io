---
title: "博客 | 网站统计功能"
date: 2025-12-11T14:23:32+08:00
draft: false
categories:
    - 博客

---
## 一些实现方式

目前看到网上关于网站统计功能的实现方式：
- 基于busuanzi js的统计功能
- 基于Waline 的统计功能
- 基于服务器端的统计功能

关于上面的两种方式大家可以自行在网上搜索，这里就不展开讲了，主要讲一下基于自行服务端的统计功能。


## 基于服务器端的统计功能
### 优点
- 数据源真实可靠（全部来自你自己的数据库）
- 访问量可以根据业务逻辑定义
- 可以进行强一致性统计（文章访问量、文章数量、评论数量等）
- 不依赖第三方服务
- 后续可以接入监控告警系统，实时观察
- 后续可以在自研管理平台展示

## 目前统计功能
- 网站访问量
- 文章访问量
- 文章总访问量
- 网站运行时间
- .... 

## 实现方式
采用gin web 框架
https://github.com/gin-gonic/gin

使用 GORM 做数据库对象关系映射
https://github.com/go-gorm/gorm

以处理POST /api/article/visit，其他接口处理基本相同

```go
func (r *articleRepo) IncreaseViewCount(path string) (int64, error) {
	// 1. 执行 Upsert (存在则更新，不存在则插入)，体现原子性操作，避免并发问题
	// SQL: INSERT INTO article_stats ... ON DUPLICATE KEY UPDATE view_count = view_count + 1
	err := r.db.Clauses(clause.OnConflict{
		Columns:   []clause.Column{{Name: "path"}},
		DoUpdates: clause.Assignments(map[string]interface{}{
			"view_count": gorm.Expr("view_count + 1"),
		}),
	}).Create(&model.ArticleStat{Path: path, ViewCount: 1}).Error

	if err != nil {
		return 0, err
	}

	// 2. 查出最新的值返回
	var stat model.ArticleStat
	err = r.db.Select("view_count").Where("path = ?", path).First(&stat).Error
	return stat.ViewCount, err
}
```

前端逻辑
上报/article/visit 接口时如果是首页(/)或者分页(/page/1)或者搜索(/search/query)，也会添加到文章计数，这里排除了这个bug
```js
        <script>
            (function() {
                const isLocal = ["localhost", "127.0.0.1"].includes(window.location.hostname);
        
                const API_URL = isLocal 
                    ? "http://localhost:8080/api/article/visit" 
                    : "https://hangops.top/api/article/visit"; 
                
                const path = window.location.pathname;
                // 如果是首页(/)或者分页(/page/1)或者搜索(/search/query)，直接什么都不做
                if (path === "/" || 
                    path.includes("/page/") || 
                    path.includes("/search/")) {
                    return;
                }

                fetch(API_URL, {
                    method: 'POST', 
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ path: path }) 
                })
                .then(response => response.json()) 
                .then(data => {
                    const container = document.getElementById("article_views_container");
                    const viewEl = document.getElementById("article_views");
                    
                    if (container && viewEl && data.views) {
                        viewEl.innerText = data.views;
                        
                        container.style.display = "flex";
                    }
                })
                .catch(err => {
                    console.error("阅读量获取失败:", err);
                });
            })();
        </script>       
```




