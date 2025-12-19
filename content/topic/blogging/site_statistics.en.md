---
categories:
- Blog
date: 2025-12-11 06:23:32
draft: false
title: Hugo | How to Custom Implement Website Statistics
---

## Some Implementation Methods

Currently, there are several ways to implement website statistics functionality that I have seen on the internet:
- Statistics based on busuanzi js
- Statistics based on Waline
- Statistics based on server-side statistics

You can search for information about the above two methods on the internet, and I will not elaborate on them here. Instead, I will mainly discuss the implementation of statistics based on a self-service server.

## Server-Side Statistics Implementation
### Advantages
- Data source is real and reliable (all from your own database)
- Traffic volume can be defined according to business logic
- Strong consistency statistics can be performed (article views, article count, comment count, etc.)
- Does not rely on third-party services
- Can be integrated with monitoring and alerting systems for real-time observation
- Can be displayed on self-developed management platforms

## Current Statistics Functionality
- Website traffic
- Article views
- Total article views
- Website uptime
- ...

## Implementation Methods
Using the gin web framework
https://github.com/gin-gonic/gin

Using GORM for database object-relational mapping
https://github.com/go-gorm/gorm

Processing POST /api/article/visit, other interfaces are handled similarly

```go
func (r *articleRepo) IncreaseViewCount(path string) (int64, error) {
	// 1. Execute Upsert (update if exists, insert if not), demonstrating atomic operations to avoid concurrency issues
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

	// 2. Retrieve the latest value and return it
	var stat model.ArticleStat
	err = r.db.Select("view_count").Where("path = ?", path).First(&stat).Error
	return stat.ViewCount, err
}
```

Front-end logic
When reporting the /article/visit API, if it is the homepage (/) or pagination (/page/1) or search (/search/query), it will also be added to the article count, and this bug is excluded
```js
        <script>
            (function() {
                const isLocal = ["localhost", "127.0.0.1"].includes(window.location.hostname);
        
                const API_URL = isLocal 
                    ? "http://localhost:8080/api/article/visit" 
                    : "https://hangops.top/api/article/visit"; 
                
                const path = window.location.pathname;
                // If it is the homepage (/) or pagination (/page/1) or search (/search/query), do nothing directly
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
                    console.error("Failed to retrieve view count:", err);
                });
            })();
        </script>       
```